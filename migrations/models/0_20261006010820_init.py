from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `demo` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(150) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL COMMENT '用户密码'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `oa_users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(150) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL COMMENT '用户密码',
    `is_active` BOOL NOT NULL COMMENT '是否是活跃用户',
    `email` VARCHAR(32) COMMENT '邮箱',
    `nick_name` VARCHAR(32) UNIQUE COMMENT '用户昵称',
    `gender` VARCHAR(16) COMMENT '性别',
    `phone` VARCHAR(11) UNIQUE COMMENT '电话号码',
    `avatar` VARCHAR(64) NOT NULL COMMENT '头像',
    `enabled` BOOL NOT NULL COMMENT '是否启用？状态：1启用，0禁用',
    `is_superuser` BOOL NOT NULL COMMENT '是否是超级用户'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `oa_online_user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
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
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztml1vozgUhv9KxdWs1J3lO2Tukk6r7c5MI7Wd1UibFTJgEhRiM2DaqWbz39c2EL5TSN"
    "uU7eYmosfngP0c+/XB9Kewxg70o/cf4RoLH05+CgisIb0o2U9PBBAEuZUZCLB87uhkHlZE"
    "QmATanOBH8FT1hTZoRcQDyNqRbHvMyO2qaOHFrkpRt73GJoELyBZwpA2/PU3NXvIgT9glP"
    "0ZrEzXg75T6qbnsGdzu0keAm67ROSCO7KnWaaN/XiNcufggSwx2np7iDDrAiIYAgLZ7UkY"
    "s+6z3qWjzEaU9DR3SbpYiHGgC2KfFIZrmblNMM2r2a15c35rmkIPQDZGDC7tasRHv2Bd+F"
    "WW1JFqKLpqUBfeza1ltEkenYNJAjmeq1thw9sBAYkHZ5xDjSMY8usa2rMlCJvZFmMqhGnX"
    "q4QznodGLMzjkSYb81iXldE81lQxGcnjyNfgh+lDtCBL+qekiTsA/zm5Pvt9cv2Oev3C7o"
    "7pskjWylXaJCdtLAs59QBE0T0OGyZ0O/VizPNQzww59nw1Px93y9apxRClvejLRhf6stFO"
    "n7VtNkxV3FVhCTCDBezVPQgds9aCZdzmW29ay+uqBSCw4ETZINkIUo2dId9D8GvEla+mwI"
    "XWnTqMgYm5qxlnvkdFfiuKbIX4PklqV2XII/bShRTey8uC7qjuPDbGNhUHTdeNVxWEohx7"
    "QR/cifewURcVeKSPLArc1bSk532R62oH4rraCpw1lXmv4EMf4Kn7sIlrlmYUuRO8gmgf3L"
    "KmdeBNvVqB87YycbZPmL3kuhDxuGa/KnjVsKsT3lDnsQpFkaXFHdPfsQQ65uIZ1L1Wa5Tz"
    "UE/CBQ6ht0Cf4APPxSXtEUB2U32dFgqsRLhELn67edhk8zGz5kMJwf22FilOU4qJwoEkUZ"
    "PJzdnk47mweZ06b5ughiqvmLydNR4bW3Ss7t5UdXd83z6+b/8f3rdL5XVkUvHy7hom/RRj"
    "HwLUoinFuEoKLBr4UjnIFkO/lxtddtmsl/XsWncUWncbjq0UM9Rr+2tKwnQ2+8xuso6i7z"
    "43XN5WkvH1y/ScZonniDp5yZaYiVOeGLgGnt9nTWwDhl2Lj0UAKXPL2msNKHKHJaDIrSuA"
    "NZU5I89emX1VvxT0LLwPoPq6rmjUMnbFYZCnhJx+hyl5xLDnuC7KTO1l2dpL5/UuMq+3q7"
    "xe22Ipq17zexsw7LnN5rNhOQ5lrbijJ+ysUhfiUjtxqUoc3NEis9fcziMOV9CkD/0ttbwP"
    "KLHeadDGCn2T1ETbHcYBFkQMSUM5ubOeKUT9l6oZ+utmKu+6EruWLVbliKLELUCqOom2yH"
    "YBQ0pMQ6p5aFEZxQEMm09iHqtHS6EHTOLW8sSa1HAMtj9DMBpSTdrj41yeyPJHsKghl+kN"
    "Lj5dQx9wKvWkNX55G8oef5gjtc1LHoRNYOjZS6HhGCxtOd11CAZyn+MR2BPn02COwO7oak"
    "0XY9fCpRAy5KOY7ohf/osPW1R9SsNg/6+aw6YriZ0OFMUdB4pi7UCRPpHAZGmXCf9xM7tq"
    "JlwIqVB2PJuc/HPie1GXD2tDo70DLoNRKgsypu++TL5VcZ99nk05HByRRcjvwm8wfe3/3t"
    "n8C7vbCuo="
)
