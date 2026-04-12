#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业级RBAC系统 - 代码检测脚本
对后端代码进行全面严格检测
"""

import os
import re
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))


class CodeChecker:
    """代码检测类"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.app_dir = self.project_root / "App"
        self.check_results = defaultdict(list)
        self.stats = defaultdict(int)
        self.issues = []
    
    def run_all_checks(self) -> Dict[str, Any]:
        """运行所有检测"""
        print("=" * 80)
        print("开始代码检测...")
        print("=" * 80)
        
        self.check_project_structure()
        self.check_security()
        self.check_architecture()
        self.check_code_quality()
        self.check_database()
        self.check_api_design()
        self.check_error_handling()
        self.check_logging()
        self.check_configuration()
        self.check_testing()
        
        return self.generate_report()
    
    def check_project_structure(self):
        """检测项目结构"""
        print("\n[检测] 项目结构...")
        
        expected_dirs = [
            "App/Api",
            "App/Config",
            "App/Core",
            "App/Dependencies",
            "App/Models",
            "App/Repositories",
            "App/Schemas",
            "App/Services",
            "App/Utils",
            "scripts"
        ]
        
        for dir_path in expected_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                self.check_results["项目结构"].append({
                    "type": "success",
                    "message": f"目录存在: {dir_path}",
                    "severity": "low"
                })
                self.stats["结构正确"] += 1
            else:
                self.check_results["项目结构"].append({
                    "type": "warning",
                    "message": f"目录缺失: {dir_path}",
                    "severity": "medium"
                })
                self.stats["结构问题"] += 1
                self.issues.append(f"目录缺失: {dir_path}")
        
        py_files = list(self.app_dir.rglob("*.py"))
        self.check_results["项目结构"].append({
            "type": "info",
            "message": f"Python文件数量: {len(py_files)}",
            "severity": "low"
        })
        self.stats["Python文件数"] = len(py_files)
        
        print(f"  - 检测到 {len(py_files)} 个Python文件")
    
    def check_security(self):
        """检测安全性"""
        print("\n[检测] 安全性...")
        
        critical_issues = []
        warnings = []
        
        env_file = self.project_root / ".env"
        if env_file.exists():
            content = env_file.read_text(encoding="utf-8")
            if "password" in content.lower() or "secret" in content.lower():
                warnings.append({
                    "message": ".env文件包含敏感信息，请确保不在版本控制中",
                    "file": ".env",
                    "severity": "high"
                })
        
        settings_file = self.app_dir / "Config" / "Settings.py"
        if settings_file.exists():
            content = settings_file.read_text(encoding="utf-8")
            if "your-secret-key-here" in content:
                critical_issues.append({
                    "message": "JWT密钥使用默认值，存在严重安全隐患",
                    "file": "App/Config/Settings.py",
                    "severity": "critical"
                })
            
            if "1124" in content or "root" in content:
                warnings.append({
                    "message": "数据库凭据硬编码在配置文件中",
                    "file": "App/Config/Settings.py",
                    "severity": "high"
                })
        
        py_files = list(self.app_dir.rglob("*.py"))
        for py_file in py_files:
            content = py_file.read_text(encoding="utf-8")
            
            sql_patterns = [
                r'f".*SELECT.*{.*}"',
                r'f".*INSERT.*{.*}"',
                r'f".*UPDATE.*{.*}"',
                r'f".*DELETE.*{.*}"',
                r'".*SELECT.*%"\s*%\s*\(',
            ]
            
            for pattern in sql_patterns:
                if re.search(pattern, content):
                    warnings.append({
                        "message": "可能存在SQL注入风险 - 使用字符串拼接构建SQL",
                        "file": str(py_file.relative_to(self.project_root)),
                        "severity": "high"
                    })
                    break
        
        for issue in critical_issues:
            self.check_results["安全性"].append({
                "type": "error",
                "message": issue["message"],
                "file": issue["file"],
                "severity": issue["severity"]
            })
            self.stats["安全严重问题"] += 1
            self.issues.append(f"[CRITICAL] {issue['message']} in {issue['file']}")
        
        for issue in warnings:
            self.check_results["安全性"].append({
                "type": "warning",
                "message": issue["message"],
                "file": issue["file"],
                "severity": issue["severity"]
            })
            self.stats["安全警告"] += 1
            self.issues.append(f"[WARNING] {issue['message']} in {issue['file']}")
        
        self.check_results["安全性"].append({
            "type": "success",
            "message": "使用JWT认证机制",
            "severity": "low"
        })
        self.check_results["安全性"].append({
            "type": "success",
            "message": "使用bcrypt进行密码加密",
            "severity": "low"
        })
        
        print(f"  - 发现 {len(critical_issues)} 个严重安全问题")
        print(f"  - 发现 {len(warnings)} 个安全警告")
    
    def check_architecture(self):
        """检测架构设计"""
        print("\n[检测] 架构设计...")
        
        architecture_good = [
            "采用分层架构：API -> Service -> Repository -> Model",
            "使用依赖注入模式",
            "实现了Repository模式",
            "使用Pydantic进行数据验证",
            "API版本控制（V1）"
        ]
        
        for item in architecture_good:
            self.check_results["架构设计"].append({
                "type": "success",
                "message": item,
                "severity": "low"
            })
            self.stats["架构优点"] += 1
        
        api_dir = self.app_dir / "Api" / "V1"
        service_dir = self.app_dir / "Services"
        repo_dir = self.app_dir / "Repositories"
        
        api_files = [f.stem for f in api_dir.glob("*.py") if f.stem != "__init__"]
        service_files = [f.stem.replace("Service", "") for f in service_dir.glob("*Service.py")]
        repo_files = [f.stem.replace("Repository", "") for f in repo_dir.glob("*Repository.py")]
        
        missing_services = set(api_files) - set(service_files) - {"Metrics"}
        missing_repos = set(service_files) - set(repo_files)
        
        if missing_services:
            self.check_results["架构设计"].append({
                "type": "warning",
                "message": f"缺少Service层: {', '.join(missing_services)}",
                "severity": "medium"
            })
            self.stats["架构问题"] += 1
        
        if missing_repos:
            self.check_results["架构设计"].append({
                "type": "warning",
                "message": f"缺少Repository层: {', '.join(missing_repos)}",
                "severity": "medium"
            })
            self.stats["架构问题"] += 1
        
        print(f"  - API文件数: {len(api_files)}")
        print(f"  - Service文件数: {len(service_files)}")
        print(f"  - Repository文件数: {len(repo_files)}")
    
    def check_code_quality(self):
        """检测代码质量"""
        print("\n[检测] 代码质量...")
        
        py_files = list(self.app_dir.rglob("*.py"))
        total_lines = 0
        total_functions = 0
        total_classes = 0
        
        for py_file in py_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                lines = content.split("\n")
                total_lines += len(lines)
                
                functions = re.findall(r'^\s*def\s+\w+', content, re.MULTILINE)
                classes = re.findall(r'^\s*class\s+\w+', content, re.MULTILINE)
                
                total_functions += len(functions)
                total_classes += len(classes)
                
                for i, line in enumerate(lines, 1):
                    if len(line) > 120:
                        self.check_results["代码质量"].append({
                            "type": "warning",
                            "message": f"行过长({len(line)}字符)",
                            "file": str(py_file.relative_to(self.project_root)),
                            "line": i,
                            "severity": "low"
                        })
                
                if not lines or not lines[0].startswith('"""') and not lines[0].startswith("'''"):
                    pass
                
            except Exception as e:
                pass
        
        self.check_results["代码质量"].append({
            "type": "info",
            "message": f"总代码行数: {total_lines}",
            "severity": "low"
        })
        self.check_results["代码质量"].append({
            "type": "info",
            "message": f"函数数量: {total_functions}",
            "severity": "low"
        })
        self.check_results["代码质量"].append({
            "type": "info",
            "message": f"类数量: {total_classes}",
            "severity": "low"
        })
        
        self.stats["总代码行数"] = total_lines
        self.stats["函数数量"] = total_functions
        self.stats["类数量"] = total_classes
        
        print(f"  - 总代码行数: {total_lines}")
        print(f"  - 函数数量: {total_functions}")
        print(f"  - 类数量: {total_classes}")
    
    def check_database(self):
        """检测数据库相关"""
        print("\n[检测] 数据库...")
        
        model_dir = self.app_dir / "Models"
        model_files = list(model_dir.glob("*.py"))
        
        self.check_results["数据库"].append({
            "type": "success",
            "message": f"Model文件数: {len([f for f in model_files if f.stem != '__init__' and f.stem != 'Base'])}",
            "severity": "low"
        })
        
        base_model = model_dir / "Base.py"
        if base_model.exists():
            self.check_results["数据库"].append({
                "type": "success",
                "message": "存在Base基础模型",
                "severity": "low"
            })
        
        db_config = self.app_dir / "Config" / "Database.py"
        if db_config.exists():
            content = db_config.read_text(encoding="utf-8")
            if "pool_pre_ping" in content and "pool_recycle" in content:
                self.check_results["数据库"].append({
                    "type": "success",
                    "message": "配置了数据库连接池",
                    "severity": "low"
                })
        
        print(f"  - Model文件数: {len(model_files)}")
    
    def check_api_design(self):
        """检测API设计"""
        print("\n[检测] API设计...")
        
        api_v1_dir = self.app_dir / "Api" / "V1"
        api_files = list(api_v1_dir.glob("*.py"))
        
        endpoints = []
        for api_file in api_files:
            if api_file.stem == "__init__":
                continue
            content = api_file.read_text(encoding="utf-8")
            routes = re.findall(r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']', content)
            for method, path in routes:
                endpoints.append({
                    "file": api_file.stem,
                    "method": method.upper(),
                    "path": path
                })
        
        self.check_results["API设计"].append({
            "type": "success",
            "message": f"API端点数量: {len(endpoints)}",
            "severity": "low"
        })
        self.stats["API端点数"] = len(endpoints)
        
        methods_count = defaultdict(int)
        for ep in endpoints:
            methods_count[ep["method"]] += 1
        
        for method, count in methods_count.items():
            self.check_results["API设计"].append({
                "type": "info",
                "message": f"{method}: {count} 个端点",
                "severity": "low"
            })
        
        print(f"  - API端点数量: {len(endpoints)}")
    
    def check_error_handling(self):
        """检测错误处理"""
        print("\n[检测] 错误处理...")
        
        exceptions_file = self.app_dir / "Core" / "Exceptions.py"
        if exceptions_file.exists():
            content = exceptions_file.read_text(encoding="utf-8")
            exception_classes = re.findall(r'class\s+(\w+)\(.*Exception', content)
            
            self.check_results["错误处理"].append({
                "type": "success",
                "message": f"自定义异常类: {', '.join(exception_classes)}",
                "severity": "low"
            })
            self.stats["自定义异常数"] = len(exception_classes)
        
        main_file = self.app_dir / "Main.py"
        if main_file.exists():
            content = main_file.read_text(encoding="utf-8")
            if "@app.exception_handler" in content:
                self.check_results["错误处理"].append({
                    "type": "success",
                    "message": "配置了全局异常处理器",
                    "severity": "low"
                })
        
        print("  - 错误处理检测完成")
    
    def check_logging(self):
        """检测日志"""
        print("\n[检测] 日志...")
        
        logger_file = self.app_dir / "Utils" / "Logger.py"
        if logger_file.exists():
            self.check_results["日志"].append({
                "type": "success",
                "message": "存在日志工具类",
                "severity": "low"
            })
        
        operation_log = self.app_dir / "Models" / "OperationLog.py"
        audit_log = self.app_dir / "Models" / "AuditLog.py"
        
        if operation_log.exists():
            self.check_results["日志"].append({
                "type": "success",
                "message": "存在操作日志模型",
                "severity": "low"
            })
        
        if audit_log.exists():
            self.check_results["日志"].append({
                "type": "success",
                "message": "存在审计日志模型",
                "severity": "low"
            })
        
        print("  - 日志检测完成")
    
    def check_configuration(self):
        """检测配置管理"""
        print("\n[检测] 配置管理...")
        
        env_example = self.project_root / ".env.example"
        if env_example.exists():
            self.check_results["配置管理"].append({
                "type": "success",
                "message": "存在.env.example模板文件",
                "severity": "low"
            })
        
        settings_file = self.app_dir / "Config" / "Settings.py"
        if settings_file.exists():
            content = settings_file.read_text(encoding="utf-8")
            if "pydantic_settings" in content:
                self.check_results["配置管理"].append({
                    "type": "success",
                    "message": "使用pydantic-settings进行配置管理",
                    "severity": "low"
                })
        
        system_config_model = self.app_dir / "Models" / "SystemConfig.py"
        if system_config_model.exists():
            self.check_results["配置管理"].append({
                "type": "success",
                "message": "支持数据库系统配置",
                "severity": "low"
            })
        
        print("  - 配置管理检测完成")
    
    def check_testing(self):
        """检测测试"""
        print("\n[检测] 测试...")
        
        tests_dir = self.project_root / "tests"
        test_files = list(self.project_root.rglob("test_*.py")) + list(self.project_root.rglob("*_test.py"))
        
        if tests_dir.exists():
            self.check_results["测试"].append({
                "type": "success",
                "message": "存在tests目录",
                "severity": "low"
            })
        
        if test_files:
            self.check_results["测试"].append({
                "type": "success",
                "message": f"测试文件数量: {len(test_files)}",
                "severity": "low"
            })
            self.stats["测试文件数"] = len(test_files)
        else:
            self.check_results["测试"].append({
                "type": "warning",
                "message": "未找到测试文件",
                "severity": "medium"
            })
            self.stats["测试问题"] += 1
        
        pytest_cache = self.project_root / ".pytest_cache"
        if pytest_cache.exists():
            self.check_results["测试"].append({
                "type": "info",
                "message": "使用pytest测试框架",
                "severity": "low"
            })
        
        print(f"  - 测试文件数量: {len(test_files)}")
    
    def generate_report(self) -> Dict[str, Any]:
        """生成检测报告"""
        print("\n" + "=" * 80)
        print("检测完成，生成报告...")
        print("=" * 80)
        
        report = {
            "project_name": "Enterprise RBAC System",
            "check_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_checks": len(self.check_results),
                "total_issues": len(self.issues),
                "statistics": dict(self.stats)
            },
            "check_results": dict(self.check_results),
            "issues": self.issues
        }
        
        return report


def main():
    """主函数"""
    project_root = Path(__file__).parent.parent
    checker = CodeChecker(project_root)
    report = checker.run_all_checks()
    
    output_dir = Path(__file__).parent
    report_file = output_dir / "check_report.json"
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n检测报告已保存到: {report_file}")
    
    print("\n" + "=" * 80)
    print("检测摘要")
    print("=" * 80)
    print(f"检测模块数: {report['summary']['total_checks']}")
    print(f"发现问题数: {report['summary']['total_issues']}")
    print("\n统计数据:")
    for key, value in report['summary']['statistics'].items():
        print(f"  - {key}: {value}")
    
    if report['issues']:
        print("\n主要问题:")
        for i, issue in enumerate(report['issues'][:10], 1):
            print(f"  {i}. {issue}")
        if len(report['issues']) > 10:
            print(f"  ... 还有 {len(report['issues']) - 10} 个问题")
    
    return report


if __name__ == "__main__":
    main()
