from peewee import *

db = SqliteDatabase('./thzsys.db')

SettingKey = "system_setting_key"


def DbInit():
    Right.create_table()
    Role.create_table()
    User.create_table()
    CXData.create_table()
    CXGPData.create_table()
    GPData.create_table()
    SysConfig.create_table()
    SysLog.create_table()
    SampleType.create_table()
    Sample.create_table()
    Setting.create_table()


# 数据对象基类
class BaseModel(Model):
    class Meta:
        database = db


# 权限表
class Right(BaseModel):
    # 主键
    Id = AutoField()
    # 权限名字
    Name = CharField(null=False)
    # 父级Id
    ParentId = CharField(null=False)

    class Meta:
        db_table = 'right'


# 角色表
class Role(BaseModel):
    # 主键
    Id = AutoField()
    # 角色名字
    Name = CharField(null=False)
    # 权限名称 json
    Rights = TextField(null=True)
    # 备注
    Comment = CharField()

    class Meta:
        db_table = 'role'


# 角色表
class User(BaseModel):
    # 主键
    Id = AutoField()
    # 名字
    Name = CharField(null=False)
    # 手机号
    Phone = CharField(null=False)
    # 角色
    Role = CharField(null=False)
    # 角色Id
    RoleId = IntegerField()
    # 备注
    Comment = CharField(null=False)
    # 密码
    Pwd = CharField(null=False, default="888888")

    class Meta:
        db_table = 'user'


class CXData(BaseModel):
    Id = AutoField()
    XStart = DoubleField(null=True)
    XStep = DoubleField(null=True)
    XEnd = DoubleField(null=True)
    YStart = DoubleField(null=True)
    YStep = DoubleField(null=True)
    YEnd = DoubleField(null=True)
    Index = IntegerField(null=True)
    DivFreq = IntegerField(null=True)
    Angle = DoubleField(null=True)       # 入射角
    Refraction = DoubleField(null=True)  # 折射率
    Operator = CharField(null=True)
    AddDate = DateTimeField(null=True)
    SampleTypeID = IntegerField(null=True)
    SampleType = CharField(null=True)
    SampleName = CharField(null=True)
    FilePath = CharField(null=True)

    class Meta:
        db_table = 'TB_CXDATA'


class CXGPData(BaseModel):
    Id = AutoField()
    ScanTime = DoubleField(null=True)
    RunTime = DoubleField(null=True)
    Index = IntegerField(null=True)
    DivFreq = IntegerField(null=True)
    Angle = DoubleField(null=True)       # 入射角
    AvgNum = IntegerField(null=True)     # 计算次数
    Refraction = DoubleField(null=True)  # 折射率
    Thickness = DoubleField(null=True)
    Operator = CharField(null=True)
    AddDate = DateTimeField(null=True)
    Data = BlobField(null=True)
    SampleTypeID = IntegerField(null=True)
    SampleType = CharField(null=True)
    SampleName = CharField(null=True)

    class Meta:
        db_table = 'TB_CXGPDATA'


class GPData(BaseModel):
    Id = AutoField()
    Start = DoubleField(null=True)
    Step = DoubleField(null=True)
    End = DoubleField(null=True)
    Thickness = DoubleField(null=True)
    Operator = CharField(null=True)
    AddDate = DateTimeField(null=True)
    Data = BlobField(null=True)
    SampleTypeID = IntegerField(null=True)
    SampleType = CharField(null=True)
    SampleName = CharField(null=True)

    class Meta:
        db_table = 'TB_GPDATA'


class SysConfig(BaseModel):
    Id = AutoField()
    Type = IntegerField(null=True)
    AddDate = DateTimeField(null=True)
    Name = CharField(null=True)
    Comment = CharField(null=True)
    File = CharField(null=True)

    class Meta:
        db_table = 'TB_SysConfig'


class SysLog(BaseModel):
    Id = AutoField()
    Type = CharField(null=True)
    UserId = IntegerField(null=True)
    Level = IntegerField(null=True)
    AddDate = DateTimeField(null=True)
    Context = TextField(null=True)

    class Meta:
        db_table = 'TB_SysLog'


class SampleType(BaseModel):
    Id = AutoField()
    ParentId = IntegerField(null=True)
    Name = CharField(null=True)
    Note = CharField(null=True)
    Path = CharField(null=True)

    class Meta:
        db_table = 'TB_Sample_type'


class Sample(BaseModel):
    Id = AutoField()
    No = CharField(null=False)
    TypeId = IntegerField(null=False)
    Model = IntegerField(null=False, default=0)
    Code = CharField(null=False, default="QT002")
    Name = CharField(null=True)
    AddDate = DateTimeField(null=True)
    Note = CharField(null=True)
    FData = BlobField(null=True)
    RData = BlobField(null=True)

    class Meta:
        db_table = 'TB_Sample'


class Setting(BaseModel):
    ConfigKey = CharField(null=False)
    LogSaveTime = CharField(null=False, default="一周")
    DataSaveTime = CharField(null=False, default="一周")
    DataBaseType = CharField(null=False, default="光谱")
    DataSavePath = CharField(null=True)

    class Meta:
        db_table = 'TB_Setting'
