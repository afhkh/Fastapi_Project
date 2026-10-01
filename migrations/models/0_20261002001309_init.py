from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `demo` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(150) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL COMMENT '用户密码'
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
    "eJztlWtv0zAUhv9KlU9DGijNeon2rSsgQNBKW4WQVmQ5iZtYdezMdtim0f+Oj9POSW+0aO"
    "Iy8S15z2v7nCc5xw9eLhLC1KvXJBfeeevB4zgn5qGhn7Y8XBROBUHjiFljsnJESksca6PN"
    "MFPkFEIqlrTQVHCj8pIxEEVsjJSnTio5vSkJ0iIlOiPSBK6/GpnyhNwRtXot5mhGCUsaad"
    "IEzrY60veF1d5z/dYa4bQIxYKVOXfm4l5ngj+6KdegpoQTiTWB7bUsIX3IblnlqqIqU2ep"
    "UqytScgMl0zXyo2Q0zyERuMJunozQcg7AlAsOMA1qSpbfQopvAzanX4nPOt1QmOxaT4q/U"
    "V1tANTLbR4RhNvYeNY48phGTuopSLSPm+gHWZYbmdbX7NG2KS+TnjF83cj9qZlvxuE07IX"
    "nPWnZbfjV5X8HHmO7xAjPNWZeW13/T2APw8uh+8GlyfG9QJ2F6Ytql4ZLUNBFYOv4KgXWK"
    "lbIbf80Lup19c8DfWV4LC7bn467lHcM0rot3+JfhAeQj8Id9OH2GIBU2U2r7UACBGO57dY"
    "JmgjIgKxy7sZyoN8XcEcp5YoFAkVLGfsgEgaZ9um7zKyd/5i5/k/gZ/LBP5GpIKUjhgFtS"
    "V/8yQ4HHGj54Nu94CeN66dPW9jzYkLTXUE4aX9GdJt+wfdZ/6e+8zfuM/MiZpUrd0k/OFq"
    "PNpOuLZkjXJCY9363mJUbcyKf4D2HrgAA3bOlbphdaYnnwZf1nEPP44vLByhdCrtLnaDiz"
    "99mS1+AOh746Y="
)
