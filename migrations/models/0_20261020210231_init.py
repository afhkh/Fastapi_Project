from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `demo` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(150) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL COMMENT '用户密码'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `oa_dept` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间',
    `update_time` DATETIME(6) COMMENT '更新时间',
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除',
    `sub_count` INT COMMENT '子部门数量',
    `name` VARCHAR(64) NOT NULL UNIQUE COMMENT '部门名',
    `enabled` BOOL NOT NULL COMMENT '状态',
    `dept_sort` INT COMMENT '排序',
    `pid_id` INT COMMENT '父部门id',
    CONSTRAINT `fk_oa_dept_oa_dept_e8b89e44` FOREIGN KEY (`pid_id`) REFERENCES `oa_dept` (`id`) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COMMENT='id, 父部门id, 子部门数目, name,';
CREATE TABLE IF NOT EXISTS `oa_job` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间',
    `update_time` DATETIME(6) COMMENT '更新时间',
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除',
    `name` VARCHAR(32) COMMENT '岗位名称',
    `enabled` BOOL NOT NULL COMMENT '岗位状态',
    `job_sort` INT NOT NULL UNIQUE COMMENT '排序'
) CHARACTER SET utf8mb4 COMMENT='岗位名称， 岗位状态， 排序，';
CREATE TABLE IF NOT EXISTS `oa_menu` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间',
    `update_time` DATETIME(6) COMMENT '更新时间',
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除',
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
    `is_menu` BOOL NOT NULL COMMENT '是否是菜单',
    `pid_id` INT COMMENT '父菜单id',
    CONSTRAINT `fk_oa_menu_oa_menu_393bc584` FOREIGN KEY (`pid_id`) REFERENCES `oa_menu` (`id`) ON DELETE SET NULL
) CHARACTER SET utf8mb4 COMMENT='上级菜单id, 子菜单数目， 菜单类型， 菜单标题， 组件名称， 组件， 排序， 图标， 连接地址， 是否外链， 缓存， 隐藏';
CREATE TABLE IF NOT EXISTS `ao_role` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间',
    `update_time` DATETIME(6) COMMENT '更新时间',
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除',
    `name` VARCHAR(32) UNIQUE COMMENT '角色名',
    `level` INT COMMENT '角色级别',
    `description` VARCHAR(255) COMMENT '描述信息',
    `data_scope` VARCHAR(32) COMMENT '权限描述,唯一编码',
    `status` BOOL NOT NULL COMMENT '是否启用?状态：1启用、0禁用'
) CHARACTER SET utf8mb4 COMMENT='name, 级别， 描述， 数据权限，';
CREATE TABLE IF NOT EXISTS `oa_users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间',
    `update_time` DATETIME(6) COMMENT '更新时间',
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除',
    `username` VARCHAR(150) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL COMMENT '用户密码',
    `is_active` BOOL NOT NULL COMMENT '是否是活跃用户',
    `email` VARCHAR(32) COMMENT '邮箱',
    `nick_name` VARCHAR(32) UNIQUE COMMENT '用户昵称',
    `gender` VARCHAR(16) COMMENT '性别',
    `phone` VARCHAR(11) UNIQUE COMMENT '电话号码',
    `avatar` VARCHAR(64) NOT NULL COMMENT '头像',
    `enabled` BOOL NOT NULL COMMENT '是否启用？状态：1启用，0禁用',
    `is_superuser` BOOL NOT NULL COMMENT '是否是超级用户',
    `dept_id` INT COMMENT '部门名字',
    CONSTRAINT `fk_oa_users_oa_dept_552eab7d` FOREIGN KEY (`dept_id`) REFERENCES `oa_dept` (`id`) ON DELETE SET NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `oa_online_user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) COMMENT '创建时间',
    `update_time` DATETIME(6) COMMENT '更新时间',
    `create_by` VARCHAR(32) COMMENT '创建者',
    `update_by` VARCHAR(32) COMMENT '更新者',
    `is_delete` BOOL NOT NULL COMMENT '是否删除',
    `brower` VARCHAR(128) COMMENT '浏览器',
    `ip` VARCHAR(64) COMMENT '用户登录ip',
    `key` VARCHAR(255) COMMENT '存用户token',
    `user_id` INT COMMENT '和用户的一对多',
    CONSTRAINT `fk_oa_onlin_oa_users_0386d932` FOREIGN KEY (`user_id`) REFERENCES `oa_users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `oa_roles_depts` (
    `ao_role_id` INT NOT NULL,
    `dept_id` INT NOT NULL,
    FOREIGN KEY (`ao_role_id`) REFERENCES `ao_role` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`dept_id`) REFERENCES `oa_dept` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_oa_roles_de_ao_role_ff920d` (`ao_role_id`, `dept_id`)
) CHARACTER SET utf8mb4 COMMENT='角色和部门的关联表';
CREATE TABLE IF NOT EXISTS `oa_roles_menus` (
    `ao_role_id` INT NOT NULL,
    `menu_id` INT NOT NULL,
    FOREIGN KEY (`ao_role_id`) REFERENCES `ao_role` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`menu_id`) REFERENCES `oa_menu` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_oa_roles_me_ao_role_a5ba0a` (`ao_role_id`, `menu_id`)
) CHARACTER SET utf8mb4 COMMENT='角色和菜单的关联表';
CREATE TABLE IF NOT EXISTS `oa_users_jobs` (
    `oa_users_id` INT NOT NULL,
    `job_id` INT NOT NULL,
    FOREIGN KEY (`oa_users_id`) REFERENCES `oa_users` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`job_id`) REFERENCES `oa_job` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_oa_users_jo_oa_user_6777f0` (`oa_users_id`, `job_id`)
) CHARACTER SET utf8mb4 COMMENT='用户和岗位的关联表';
CREATE TABLE IF NOT EXISTS `oa_users_roles` (
    `oa_users_id` INT NOT NULL,
    `roles_id` INT NOT NULL,
    FOREIGN KEY (`oa_users_id`) REFERENCES `oa_users` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`roles_id`) REFERENCES `ao_role` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_oa_users_ro_oa_user_db847e` (`oa_users_id`, `roles_id`)
) CHARACTER SET utf8mb4 COMMENT='用户和角色的关联表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
    "/g8DCop5"
)
