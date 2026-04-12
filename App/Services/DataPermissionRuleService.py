"""Data Permission Rule Service"""

from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from App.Models.DataPermissionRule import DataPermissionRuleModel
from App.Core.Exceptions import ValidationException, NotFoundException
from App.Repositories.DataPermissionRuleRepository import DataPermissionRuleRepository
from App.Utils.Validators import Validators
from App.Utils.Logger import logger


class DataPermissionRuleService:
    """数据权限规则服务类"""

    def __init__(self, db: Session):
        """初始化数据权限规则服务"""
        self.db = db
        self.data_permission_rule_repository = DataPermissionRuleRepository(db)
        from App.Repositories.PermissionRepository import PermissionRepository
        self.permission_repository = PermissionRepository(db)

    def get_rule_by_id(self, rule_id: int, tenant_id: int) -> DataPermissionRuleModel:
        """根据ID获取数据权限规则"""
        rule = self.data_permission_rule_repository.get_by_id(rule_id, tenant_id=tenant_id)
        if not rule:
            raise NotFoundException(detail="数据权限规则不存在")
        return rule

    def get_rule_by_code(self, code: str, tenant_id: int) -> DataPermissionRuleModel:
        """根据编码获取数据权限规则"""
        rule = self.data_permission_rule_repository.get_by_code(code, tenant_id=tenant_id)
        if not rule:
            raise NotFoundException(detail="数据权限规则不存在")
        return rule

    def get_rules_by_permission_id(self, permission_id: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DataPermissionRuleModel]:
        """根据权限ID获取数据权限规则"""
        return self.data_permission_rule_repository.get_by_permission_id(permission_id, tenant_id=tenant_id, skip=skip, limit=limit)

    def get_rules_by_rule_type(self, rule_type: int, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DataPermissionRuleModel]:
        """根据规则类型获取数据权限规则"""
        return self.data_permission_rule_repository.get_by_rule_type(rule_type, tenant_id=tenant_id, skip=skip, limit=limit)

    def get_rules_by_resource_table(self, resource_table: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DataPermissionRuleModel]:
        """根据资源表名获取数据权限规则"""
        return self.data_permission_rule_repository.get_by_resource_table(resource_table, tenant_id=tenant_id, skip=skip, limit=limit)

    def get_active_rules(self, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DataPermissionRuleModel]:
        """获取活跃的数据权限规则"""
        return self.data_permission_rule_repository.get_active_rules(tenant_id=tenant_id, skip=skip, limit=limit)

    def search_rules(self, keyword: str, tenant_id: int, skip: int = 0, limit: int = 100) -> List[DataPermissionRuleModel]:
        """搜索数据权限规则"""
        return self.data_permission_rule_repository.search(keyword, tenant_id=tenant_id, skip=skip, limit=limit)

    def paginate_rules(
        self,
        tenant_id: int,
        keyword: str = None,
        permission_id: int = None,
        rule_type: int = None,
        status: int = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[int, List[DataPermissionRuleModel]]:
        """分页查询数据权限规则"""
        return self.data_permission_rule_repository.paginate(
            tenant_id=tenant_id,
            keyword=keyword,
            permission_id=permission_id,
            rule_type=rule_type,
            status=status,
            page=page,
            page_size=page_size
        )

    def create_rule(self, rule_data: Dict[str, Any], tenant_id: int, created_by: int) -> DataPermissionRuleModel:
        """创建数据权限规则"""
        code = rule_data.get("code")
        existing_rule = self.data_permission_rule_repository.get_by_code(code, tenant_id=tenant_id)
        if existing_rule:
            raise ValidationException(detail="数据权限规则编码已存在")

        name = rule_data.get("name")

        permission_id = rule_data.get("permission_id")
        permission = self.permission_repository.get_by_id(permission_id, tenant_id=tenant_id)
        if not permission:
            raise ValidationException(detail="关联的权限不存在")

        rule_type = rule_data.get("rule_type")
        if rule_type == 4 and not rule_data.get("rule_expression"):
            raise ValidationException(detail="自定义规则类型必须提供规则表达式")

        rule = DataPermissionRuleModel(
            name=name,
            code=code,
            permission_id=permission_id,
            resource_table=rule_data.get("resource_table"),
            rule_type=rule_type,
            rule_expression=rule_data.get("rule_expression"),
            description=rule_data.get("description"),
            status=rule_data.get("status", 1),
            tenant_id=tenant_id,
            created_by=created_by,
            updated_by=created_by
        )

        created_rule = self.data_permission_rule_repository.create(rule)

        logger.info(f"创建数据权限规则成功: {name}")

        return created_rule

    def update_rule(self, rule_id: int, rule_data: Dict[str, Any], tenant_id: int, updated_by: int) -> DataPermissionRuleModel:
        """更新数据权限规则"""
        rule = self.data_permission_rule_repository.get_by_id(rule_id, tenant_id=tenant_id)
        if not rule:
            raise NotFoundException(detail="数据权限规则不存在")

        code = rule_data.get("code")
        if code and code != rule.code:
            existing_rule = self.data_permission_rule_repository.get_by_code(code, tenant_id=tenant_id)
            if existing_rule:
                raise ValidationException(detail="数据权限规则编码已存在")
            rule.code = code

        if "name" in rule_data:
            rule.name = rule_data.get("name")

        if "permission_id" in rule_data:
            permission_id = rule_data.get("permission_id")
            permission = self.permission_repository.get_by_id(permission_id, tenant_id=tenant_id)
            if not permission:
                raise ValidationException(detail="关联的权限不存在")
            rule.permission_id = permission_id

        if "resource_table" in rule_data:
            rule.resource_table = rule_data.get("resource_table")

        if "rule_type" in rule_data:
            rule_type = rule_data.get("rule_type")
            if rule_type == 4 and rule_data.get("rule_expression") is None:
                if not rule.rule_expression:
                    raise ValidationException(detail="自定义规则类型必须提供规则表达式")
            rule.rule_type = rule_type

        if "rule_expression" in rule_data:
            rule.rule_expression = rule_data.get("rule_expression")

        if "description" in rule_data:
            rule.description = rule_data.get("description")

        if "status" in rule_data:
            rule.status = rule_data.get("status")

        rule.updated_by = updated_by

        updated_rule = self.data_permission_rule_repository.update(rule)

        logger.info(f"更新数据权限规则成功: {rule.name}")

        return updated_rule

    def delete_rule(self, rule_id: int, tenant_id: int) -> bool:
        """删除数据权限规则"""
        rule = self.data_permission_rule_repository.get_by_id(rule_id, tenant_id=tenant_id)
        if not rule:
            raise NotFoundException(detail="数据权限规则不存在")

        self.data_permission_rule_repository.delete(rule)

        logger.info(f"删除数据权限规则成功: {rule.name}")

        return True

    def update_rule_status(self, rule_id: int, status: int, tenant_id: int, updated_by: int) -> DataPermissionRuleModel:
        """更新数据权限规则状态"""
        if not Validators.is_status_valid(status):
            raise ValidationException(detail="无效的状态值")

        rule = self.data_permission_rule_repository.get_by_id(rule_id, tenant_id=tenant_id)
        if not rule:
            raise NotFoundException(detail="数据权限规则不存在")

        rule.status = status
        rule.updated_by = updated_by

        updated_rule = self.data_permission_rule_repository.update(rule)

        logger.info(f"更新数据权限规则状态成功: {rule.name}, 状态: {status}")

        return updated_rule

    def test_rule(self, rule_id: int, tenant_id: int) -> Dict[str, Any]:
        """测试数据权限规则"""
        rule = self.data_permission_rule_repository.get_by_id(rule_id, tenant_id=tenant_id)
        if not rule:
            raise NotFoundException(detail="数据权限规则不存在")

        if rule.status != 1:
            raise ValidationException(detail="规则未启用，无法测试")

        test_result = {
            "rule_id": rule.id,
            "rule_name": rule.name,
            "rule_code": rule.code,
            "rule_type": rule.rule_type,
            "resource_table": rule.resource_table,
            "is_valid": True,
            "message": "规则配置正确"
        }

        if rule.rule_type == 4 and rule.rule_expression:
            try:
                from sqlalchemy import text
                test_query = f"SELECT 1 FROM {rule.resource_table} WHERE 1=1 AND ({rule.rule_expression}) LIMIT 1"
                self.db.execute(text(test_query))
                test_result["message"] = "规则表达式语法正确"
            except Exception as e:
                test_result["is_valid"] = False
                test_result["message"] = f"规则表达式语法错误: {str(e)}"

        return test_result
