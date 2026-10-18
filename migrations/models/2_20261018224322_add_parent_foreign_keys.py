from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `oa_dept` ADD `pid_id` INT COMMENT '父部门id';
        ALTER TABLE `oa_menu` ADD `pid_id` INT COMMENT '父菜单id';
        ALTER TABLE `oa_dept` ADD CONSTRAINT `fk_oa_dept_oa_dept_e8b89e44` FOREIGN KEY (`pid_id`) REFERENCES `oa_dept` (`id`) ON DELETE SET NULL;
        ALTER TABLE `oa_menu` ADD CONSTRAINT `fk_oa_menu_oa_menu_393bc584` FOREIGN KEY (`pid_id`) REFERENCES `oa_menu` (`id`) ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `oa_menu` DROP FOREIGN KEY `fk_oa_menu_oa_menu_393bc584`;
        ALTER TABLE `oa_dept` DROP FOREIGN KEY `fk_oa_dept_oa_dept_e8b89e44`;
        ALTER TABLE `oa_dept` DROP COLUMN `pid_id`;
        ALTER TABLE `oa_menu` DROP COLUMN `pid_id`;"""


MODELS_STATE = (
    "eJztXFtv2zYU/iuBnzrA22TdtZchSVuslyRAmw4DlkGgJMrRIkuqLmmDzv99JGWJlEzZku"
    "ML3folcA55KOo7R+fGI30bzWIPhtkvL+EsHv129m0UgRlEPxr08dkIJAmlYkIOnJBM9KoZ"
    "TpanwM0RzQdhBsd4KHPTIMmDOELUqAhDTIxdNDGIppRURMHnAtp5PIX5PUzRwN//IHIQef"
    "ArzKp/kwfbD2DoNbYZePjahG7nTwmhvYny12Qivppju3FYzCI6OXnK7+Oonh1EOaZOYQRT"
    "kEO8fJ4WePt4d4u7rO6o3CmdUm6R4fGgD4owZ27XsSltZNvXN7f2x1e3tj0aAJAbRxhctN"
    "WM3P0Ub+FneaIaqqnoqommkG3WFGNeXpoCUzISeK5vR3MyDnJQziAYU1CLDKbk9xK0l/cg"
    "5WPL8rQQRltvI1zhuW+IR3eFocnmXaHLinFXaKpU3sl6yGfgqx3CaJrfo38nmrQC4D/PP1"
    "z+cf7hBZr1E149Ro9F+axcL4bkcgxLgaKegCz7Eqcche5GneXZDuoVgcJOn+bt4e64OqKY"
    "0mQj9GWzD/qy2Y0+HpvPsVXxH5hHABMc4D58AalnL43Ectw1d3loJs/aFBCBKUEU3yS+g9"
    "rGJjnf9ib5atsbAySBxaR15hdZv/EZAl1WEPSWBJEwLA2aJVVzNImlIkFpBqIYOkQr4X2N"
    "25Laxnonwy+W4c8KjFpRAtMT2wbPeog5NmiB4O5NUJdWWhPX72mItiIACvhQL3sUHpYFeF"
    "MPq6s9TLyudlp4PNSEGkYYBo7VuIjjEIKIDzjD1cLcQWy7crCVHIY5WNlBlliX+jrVFQBf"
    "3Ny8x4vMsuxzSAhvbltIf7q6eIWcLBEAmhTkkK/h2D/ZWZwOMSkNHrFNiq5YMtJyaB7IgC"
    "SBZw9yhZRBbGCX44r9AbwUFzbwXgb7dZzCYBq9g08E8zdoQyByeYa6FdkdO9jzSrsqKt10"
    "Cr7UURujdAgLhAAsrQXa0Nn1p/fvR/OdBd5UciC2U2Tos2XxXYHo6TbGf3uK70O1jiAO17"
    "Q8ZIRM2cCmSDXdpgs2dFNF9ImhoDmShn6bpm4+W8AEC7uVstTIpDDEuNisGyihj1MiuAf4"
    "xEhloR21WBejxBGUQ/l9GhdTHBrgrIdI0q4XbWjV5fnHy/OXrzDdbgf385WJ2NvYGXHyME"
    "wer0nD/l3MWZuFIUm4FkqBVV/1yvAIScjyURTq+5J71hymLr0epg6nJC2lZbu4wClPEytP"
    "22vasL/0jKu3m2QPitwje1DkzuwBDx1v9lBTNkZfzFQC2dihmQTLslG8uy8Xfog8QpDy5x"
    "WMCp7bJfR1fndWTerheFUoAaTbECA9NxUPhUmaomlswZJS2YJl7RrZYcM1HPTbMB3usG5K"
    "6CqWaZn1sAFdFW/C17lumR3ucMV4n7oPq9Wry/oeJilAw/tRJPxXpevquuzjC8r4stYEx/"
    "mqT+/J8CcKuX26UUu3MBbaclHsBOIGIN5FiN9QFUzTpFM4JV449UOUvfmP5WGqVgSo/lhX"
    "08WGmW/YDgRwkIeDMoSaYSspwq7qHFzfIEaCcNCUbEd4azJJBgD0uxzvJtjLmtYDfDSrE3"
    "0y1oTfjWdJHEGeCe+WQYNJ8NyYKwph4Mdh+NDcrMFzPKb90Cc+AVp/iJJX88XWbxZhGp4L"
    "o98JQGsPAL2afzygl/lMOwESRgCB7adcD7uy/sZwCV9/46eYItXfXODeD5VAzSM8/jSHFw"
    "nz+8DzIMferwSdMgmPOqv13XWnQ0oggeksyLJgmNdtcontBprFKTHMfVZXdoeYe8p1VIpf"
    "/qbeWCj1/74bjNgS9gFPXrbdYFSdnRw72KcGIyFOJ5cbjBrFThEajLDhH95gRGoQ3Q1G9a"
    "JbajC6icIggp8ycuazdODJjI7XHHvGZKpdVHNP7949U8mFOYty0vhLKdS+oSblEDzM9FQc"
    "5Vgufi1A72sgdvTqVyPYTAbV0xLxoWbftTN0chTlI6ebbAL59t/EwLZ3AOCL6WIjXp79U9"
    "zz+KHMwIVIp7CfGBbFMxxih/FlONJUeJMcj0i4hun4FimnASGC+8pfPzO6xyHCm8iPv185"
    "9I37GTXlhmi7i/tXxnlllMoJ8erwtTu6WwSsvcI6sjx5C5f0Y2my7DB9Ty52tz7THVW2fe"
    "iKDtmiT0cf+XaXPoWZYoWZ32O7QjNL3ey90+03hoTwEYYDNLieL7bfZcGmJmJ/Xrb5jind"
    "3ACdbrGJHWCyNlf14QS35+t9WxB2H2ESQ5O5Ma+vb4UEGlyCC4DxalQYY6T3Gq7el3GO4U"
    "+e8WGT7RsfFEnmBaciufIYhTKJ/sp748xcxb9xAPp7+722CZiw43eFggawtCxzUpIOfeKy"
    "v1cxmm/mb6NY3fNl5h/vZdgKmHapunFQ0KxWMy+8tkvVzUL281+HJfJYauLbhkL0PHz68Q"
    "4vKmAGKARzQDFcIYYdX5QKsTKvrQsPnNSWLUqsPLvAOXt2OrX4rtLJ0xcDT18MFPiLgbvq"
    "UULGK3gc3JTK8h1ThF3+1j3FQU7ScxVWQocOoBvv6s9AwKm4dD8TNYPYGaglAYgwdxxBks"
    "socB/swYVElknkaiJrfXRd0UT6GgVCyBvWJEA5xNZxXZKHlRKbXlbv42T1bh+rL7lYhNUg"
    "/a4ZxNZtrM+m4+EvrSi+8Yxv8U76ID7pRnzSRhw8oiBzkG5Tjv0FNIuL/rqg/JIgxAaLQb"
    "MUnHtKvb8+evpE5i7qhaRE6K8tGuKjTKGKhq1gNCsSmPI7DNbFow3WY2yd90ytOoYSJyYd"
    "UNSlgmw2d/JK94sFXr/7gMtI/MMrbkepKD5+P60i8102eJzDNHDvR5wy2GJkvLLFg845lc"
    "CeqU/ClMAe0dM68ACaYRG5FNMf4t0XXfBDNSQ0TDbv1hUb3YnUq6AorSgoSksFRXTFnPsN"
    "jbcfb675CDMsLZS9wM3P/jsLg2yj48EDo70CXAxGIyyoMH1xdf5XG+7L9zcXBJw4y6cpWY"
    "UscHHoD/DN/weKLnvT"
)
