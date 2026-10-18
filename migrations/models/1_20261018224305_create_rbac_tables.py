from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `oa_dept` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `sub_count` INT COMMENT '子部门数量',
    `name` VARCHAR(64) NOT NULL UNIQUE COMMENT '部门名',
    `enabled` BOOL NOT NULL COMMENT '状态',
    `dept_sort` INT COMMENT '排序'
) CHARACTER SET utf8mb4 COMMENT='id, 父部门id, 子部门数目, name,';
        CREATE TABLE IF NOT EXISTS `oa_job` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(32) COMMENT '岗位名称',
    `enabled` BOOL NOT NULL COMMENT '岗位状态',
    `job_sort` INT NOT NULL UNIQUE COMMENT '排序'
) CHARACTER SET utf8mb4 COMMENT='岗位名称， 岗位状态， 排序，';
        CREATE TABLE IF NOT EXISTS `oa_menu` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `sub_count` INT COMMENT '子菜单数目',
    `type` INT COMMENT '菜单类型',
    `title` VARCHAR(32) UNIQUE COMMENT '菜单标题',
    `name` VARCHAR(255) UNIQUE COMMENT '前端组件名称',
    `component` VARCHAR(255) COMMENT '前端组件',
    `menu_sort` INT COMMENT '菜单排序',
    `icon` VARCHAR(255) COMMENT '菜单图标',
    `path` VARCHAR(255) COMMENT '菜单链接地址',
    `i_frame` BOOL NOT NULL COMMENT '是否外链',
    `cache` BOOL NOT NULL COMMENT '缓存',
    `hidden` BOOL NOT NULL COMMENT '是否隐藏',
    `permission` VARCHAR(255) COMMENT '权限',
    `is_menu` BOOL NOT NULL COMMENT '是否是菜单'
) CHARACTER SET utf8mb4 COMMENT='上级菜单id, 子菜单数目， 菜单类型， 菜单标题， 组件名称， 组件， 排序， 图标， 连接地址， 是否外链， 缓存， 隐藏';
        CREATE TABLE IF NOT EXISTS `ao_role` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(32) UNIQUE COMMENT '角色名',
    `level` INT COMMENT '角色级别',
    `description` VARCHAR(255) COMMENT '描述信息',
    `data_scope` VARCHAR(32) COMMENT '权限描述,唯一编码',
    `status` BOOL NOT NULL COMMENT '是否启用?状态：1启用、0禁用'
) CHARACTER SET utf8mb4 COMMENT='name, 级别， 描述， 数据权限，';
        ALTER TABLE `oa_users` MODIFY COLUMN `password` VARCHAR(255) NOT NULL COMMENT '用户密码';
        CREATE TABLE `oa_roles_depts` (
    `dept_id` INT NOT NULL REFERENCES `oa_dept` (`id`) ON DELETE CASCADE,
    `ao_role_id` INT NOT NULL REFERENCES `ao_role` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='角色和部门的关联表';
        CREATE TABLE `oa_roles_menus` (
    `menu_id` INT NOT NULL REFERENCES `oa_menu` (`id`) ON DELETE CASCADE,
    `ao_role_id` INT NOT NULL REFERENCES `ao_role` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='角色和菜单的关联表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `oa_users` MODIFY COLUMN `password` VARCHAR(128) NOT NULL COMMENT '用户密码';
        DROP TABLE IF EXISTS `oa_roles_menus`;
        DROP TABLE IF EXISTS `oa_menu`;
        DROP TABLE IF EXISTS `oa_roles_depts`;
        DROP TABLE IF EXISTS `oa_dept`;
        DROP TABLE IF EXISTS `ao_role`;
        DROP TABLE IF EXISTS `oa_job`;"""


MODELS_STATE = (
    "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"
    "cw=="
)
