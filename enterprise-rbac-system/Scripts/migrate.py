#!/usr/bin/env python3
"""
企业级RBAC系统 - 数据库迁移脚本
功能：一键初始化数据库表结构和导入演示数据
"""

import os
import sys
import re
import argparse
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError as e:
    print(f"错误: 缺少必要的依赖库")
    print(f"请运行: pip install pymysql python-dotenv")
    sys.exit(1)


class DatabaseMigrator:
    """数据库迁移类"""

    def __init__(self):
        """初始化"""
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = self.project_root / "Scripts"
        self.migrations_dir = self.project_root / "Migrations"

        self.schema_file = self.scripts_dir / "init_schema.sql"
        self.demo_data_file = self.migrations_dir / "demo_data.sql"

        self._load_env()
        self._parse_database_url()

    def _load_env(self):
        """加载环境变量"""
        env_file = self.project_root / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            print(f"已加载环境配置文件: {env_file}")
        else:
            print(f"警告: 未找到 .env 文件，将使用 .env.example 作为参考")
            example_env = self.project_root / ".env.example"
            if example_env.exists():
                load_dotenv(example_env)

    def _parse_database_url(self):
        """解析数据库URL"""
        self.database_url = os.getenv("DATABASE_URL", "")

        if not self.database_url:
            print("错误: 未找到 DATABASE_URL 配置")
            print("请在 .env 文件中配置 DATABASE_URL")
            sys.exit(1)

        pattern = r"mysql\+pymysql://([^:]+):([^@]+)@([^:/]+):(\d+)/([^?]+)"
        match = re.match(pattern, self.database_url)

        if match:
            self.db_user = match.group(1)
            self.db_password = match.group(2)
            self.db_host = match.group(3)
            self.db_port = int(match.group(4))
            self.db_name = match.group(5)
            print(f"数据库配置: {self.db_user}@{self.db_host}:{self.db_port}/{self.db_name}")
        else:
            print("警告: 无法解析数据库URL格式，将直接使用URL连接")
            self.db_user = ""
            self.db_password = ""
            self.db_host = ""
            self.db_port = 3306
            self.db_name = ""

    def _execute_sql_file(self, engine, sql_file, description):
        """执行SQL文件 - 使用 pymysql 直接执行以避免参数绑定问题"""
        if not sql_file.exists():
            print(f"错误: 找不到文件 {sql_file}")
            return False

        print(f"\n{'='*60}")
        print(f"开始执行: {description}")
        print(f"文件: {sql_file}")
        print(f"{'='*60}\n")

        try:
            import pymysql
            import pymysql.cursors

            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()

            statements = self._split_sql_statements(sql_content)
            total = len(statements)
            success_count = 0
            error_count = 0

            conn = pymysql.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

            try:
                cursor = conn.cursor()
                for i, statement in enumerate(statements, 1):
                    if not statement.strip():
                        continue

                    try:
                        cursor.execute(statement)
                        conn.commit()
                        success_count += 1
                        if i % 10 == 0 or i == total:
                            print(f"  进度: {i}/{total} 语句已执行 (成功: {success_count}, 错误: {error_count})")
                    except Exception as e:
                        error_count += 1
                        conn.rollback()
                        print(f"  ⚠ 语句 {i}/{total} 执行出错: {e}")
                        if len(statement) > 200:
                            print(f"    语句内容: {statement[:200]}...")
                        else:
                            print(f"    语句内容: {statement}")

                cursor.close()
                print(f"\n✓ {description} 执行完成!")
                print(f"  总计: {total} 条语句")
                print(f"  成功: {success_count} 条")
                print(f"  错误: {error_count} 条")
                return success_count > 0

            finally:
                conn.close()

        except Exception as e:
            print(f"\n✗ 读取或执行文件失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _split_sql_statements(self, sql_content):
        """分割SQL语句 - 改进版本"""
        statements = []
        current_statement = []
        in_comment_single = False
        in_comment_multi = False
        in_string = False
        string_char = ''
        escape_next = False

        lines = sql_content.split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.rstrip()
            i = 0
            line_length = len(line)

            while i < line_length:
                char = line[i]

                if escape_next:
                    current_statement.append(char)
                    escape_next = False
                    i += 1
                    continue

                if char == '\\' and in_string:
                    current_statement.append(char)
                    escape_next = True
                    i += 1
                    continue

                if in_comment_single:
                    current_statement.append(char)
                    i += 1
                    continue

                if in_comment_multi:
                    if char == '*' and i + 1 < line_length and line[i + 1] == '/':
                        in_comment_multi = False
                        current_statement.append('*/')
                        i += 2
                    else:
                        current_statement.append(char)
                        i += 1
                    continue

                if char in ('"', "'"):
                    if not in_string:
                        in_string = True
                        string_char = char
                        current_statement.append(char)
                    elif char == string_char:
                        in_string = False
                        string_char = ''
                        current_statement.append(char)
                    else:
                        current_statement.append(char)
                    i += 1
                    continue

                if not in_string:
                    if char == '-' and i + 1 < line_length and line[i + 1] == '-':
                        in_comment_single = True
                        current_statement.append('--')
                        i += 2
                        continue

                    if char == '/' and i + 1 < line_length and line[i + 1] == '*':
                        in_comment_multi = True
                        current_statement.append('/*')
                        i += 2
                        continue

                    if char == ';':
                        current_statement.append(';')
                        full_statement = ''.join(current_statement).strip()
                        if full_statement:
                            statements.append(full_statement)
                        current_statement = []
                        i += 1
                        continue

                current_statement.append(char)
                i += 1

            if in_comment_single:
                in_comment_single = False

            if current_statement:
                current_statement.append('\n')

        if current_statement:
            full_statement = ''.join(current_statement).strip()
            if full_statement:
                if not full_statement.endswith(';'):
                    full_statement += ';'
                statements.append(full_statement)

        return statements

    def create_database_if_not_exists(self):
        """如果数据库不存在则创建"""
        if not self.db_name:
            print("警告: 无法确定数据库名称，跳过创建数据库步骤")
            return True

        try:
            import pymysql

            print(f"\n检查数据库 '{self.db_name}' 是否存在...")

            conn = pymysql.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                charset='utf8mb4'
            )

            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            conn.commit()
            cursor.close()
            conn.close()

            print(f"✓ 数据库 '{self.db_name}' 已就绪")
            return True

        except ImportError:
            print("警告: 未安装 pymysql，跳过数据库创建检查")
            return True
        except Exception as e:
            print(f"警告: 检查/创建数据库时出错: {e}")
            print("将尝试直接连接...")
            return True

    def migrate_schema(self):
        """迁移表结构"""
        print("\n" + "="*60)
        print("步骤 1/2: 初始化数据库表结构")
        print("="*60)

        try:
            return self._execute_sql_file(None, self.schema_file, "数据库表结构初始化")
        except Exception as e:
            print(f"✗ 连接数据库失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def import_demo_data(self):
        """导入演示数据"""
        print("\n" + "="*60)
        print("步骤 2/2: 导入演示数据")
        print("="*60)

        if not self.demo_data_file.exists():
            print(f"警告: 找不到演示数据文件 {self.demo_data_file}")
            print("跳过演示数据导入")
            return True

        try:
            return self._execute_sql_file(None, self.demo_data_file, "演示数据导入")
        except Exception as e:
            print(f"✗ 导入演示数据失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def verify(self):
        """验证迁移结果"""
        print("\n" + "="*60)
        print("验证迁移结果")
        print("="*60)

        try:
            import pymysql

            conn = pymysql.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
                charset='utf8mb4'
            )

            try:
                cursor = conn.cursor()

                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]

                print(f"\n✓ 数据库中共有 {len(tables)} 张表:")
                for i, table in enumerate(sorted(tables), 1):
                    print(f"  {i}. {table}")

                if 'sys_user' in tables:
                    cursor.execute("SELECT COUNT(*) FROM sys_user")
                    user_count = cursor.fetchone()[0]
                    print(f"\n✓ 用户表中有 {user_count} 条记录")

                if 'sys_role' in tables:
                    cursor.execute("SELECT COUNT(*) FROM sys_role")
                    role_count = cursor.fetchone()[0]
                    print(f"✓ 角色表中有 {role_count} 条记录")

                if 'sys_permission' in tables:
                    cursor.execute("SELECT COUNT(*) FROM sys_permission")
                    perm_count = cursor.fetchone()[0]
                    print(f"✓ 权限表中有 {perm_count} 条记录")

                cursor.close()
                return True

            finally:
                conn.close()

        except Exception as e:
            print(f"✗ 验证失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run(self, schema_only=False, data_only=False):
        """执行完整迁移流程"""
        print("\n" + "="*60)
        print("企业RBAC系统 - 数据库迁移工具")
        print("="*60)

        if not self.schema_file.exists():
            print(f"错误: 找不到表结构文件 {self.schema_file}")
            return False

        success = True

        if not data_only:
            if not self.create_database_if_not_exists():
                success = False

            if success and not self.migrate_schema():
                print("\n警告: 表结构迁移遇到问题，继续尝试导入数据...")

        if not schema_only:
            if not self.import_demo_data():
                success = False

        if success:
            self.verify()
            self._print_success_info()

        return success

    def _print_success_info(self):
        """打印成功信息"""
        print("\n" + "="*60)
        print("数据库迁移完成!")
        print("="*60)
        print("\n默认登录账号:")
        print("  用户名: admin")
        print("  密码:   admin123!")
        print("\n其他测试账号密码均为: admin123!")
        print("="*60 + "\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='企业级RBAC系统 - 数据库迁移工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python migrate.py                    # 完整迁移（表结构+演示数据）
  python migrate.py --schema-only      # 仅迁移表结构
  python migrate.py --data-only        # 仅导入演示数据
        """
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--schema-only', action='store_true', help='仅迁移表结构')
    group.add_argument('--data-only', action='store_true', help='仅导入演示数据')

    args = parser.parse_args()

    migrator = DatabaseMigrator()
    success = migrator.run(schema_only=args.schema_only, data_only=args.data_only)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
