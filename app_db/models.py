from django.db import models


# Create your models here.
class User(models.Model):
    sex_choice = (
        (0, '男'),
        (1, '女'),
    )
    id = models.AutoField(primary_key=True)  # 用户ID
    role = models.ForeignKey('Role', on_delete=models.CASCADE, default=1)  # 权限ID
    avatar = models.CharField(max_length=2083)  # 头像
    real_name = models.CharField(max_length=20)  # 真实姓名
    student_id = models.CharField(max_length=11)  # 学号 用于学生身份认证
    card_id = models.CharField(max_length=18, unique=True)  # 身份证 用于学生身份认证
    sex = models.PositiveSmallIntegerField(choices=sex_choice)  # 男0 女1
    email = models.EmailField()  # E-mail
    is_active = models.BooleanField(default=0)  # 账号是否已激活（邮箱验证）
    name = models.CharField(max_length=20, unique=True)  # 用户名
    password = models.CharField(max_length=256)  # 密码
    create_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Role(models.Model):
    # permission = (
    #     ('normal_user', '普通用户'),
    #
    # )
    id = models.AutoField(primary_key=True)  # 角色id
    role_name = models.CharField(max_length=255)  # 角色名称
    create_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_at = models.DateTimeField(auto_now=True)  # 更新时间
    # role_permission = models.TextField(choices=permission, default='[]')  # 角色拥有的权限ID(json数组形式存储permission_no)
    role_permission = models.TextField(default='[]')  # 角色拥有的权限ID(json数组形式存储permission_no)

    def __str__(self):
        return self.role_name

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "角色"
        verbose_name_plural = "角色"


class Permission(models.Model):
    id = models.AutoField(primary_key=True)  # 权限id
    permission_no = models.CharField(max_length=255, unique=True)  # 权限编号
    permission_name = models.CharField(max_length=255, blank=True)  # 权限名称 用于说明权限（最好不要为空）
    create_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return self.permission_name

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "权限"
        verbose_name_plural = "权限"


class GoodsType(models.Model):
    id = models.AutoField(primary_key=True)  # 商品分类ID
    name = models.CharField(max_length=20, unique=True)  # 分类名称
    create_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "物品分类"
        verbose_name_plural = "物品分类"


class Goods(models.Model):
    sale_way_choice = (
        (0, '一口价'),
        (1, '拍卖'),
    )
    is_new_choice = (
        (0, '非全新'),
        (1, '全新'),
    )
    status_choice = (
        (0, '未出售'),
        (1, '交易中'),
        (2, '已出售'),
    )
    goods_id = models.AutoField(primary_key=True)  # 商品 ID
    title = models.CharField(max_length=30)  # 标题
    description = models.CharField(max_length=3000)  # 商品描述
    picture = models.TextField()  # 图片URL
    sale_way = models.PositiveSmallIntegerField(choices=sale_way_choice)  # 出售方式
    is_new = models.BooleanField(choices=is_new_choice)  # 是否全新 0 非全新 1 全新
    fixed_price = models.DecimalField(max_digits=8, decimal_places=2)  # 一口价价格
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # 入手价格
    goods_type_id = models.ForeignKey('GoodsType', on_delete=models.CASCADE, blank=True, null=True)  # 商品ID
    customer_id = models.ForeignKey('User', on_delete=models.CASCADE)  # 购买者
    status = models.PositiveSmallIntegerField(choices=status_choice)  # 商品状态 0 未出售 1 交易中 2 已出售
    visits = models.PositiveIntegerField(default=0)  # 访问量
    create_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "商品标题"
        verbose_name_plural = "商品标题"


class GoodsMessage(models.Model):
    msg_id = models.AutoField(primary_key=True)  # 留言ID
    goods_id = models.ForeignKey('Goods', models.CASCADE)  # 商品ID
    send_user_id = models.ForeignKey('User', models.CASCADE, related_name='it_send_this_message')  # 发表用户ID
    recv_user_id = models.ForeignKey('User', models.CASCADE, related_name='it_recv_this_message')  # 接收用户ID
    content = models.CharField(max_length=256)  # 留言内容
    create_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "商品留言"
        verbose_name_plural = "商品留言"


class ChatRecord(models.Model):
    msg_id = models.AutoField(primary_key=True)  # 留言ID
    goods_id = models.ForeignKey('Goods', models.CASCADE)  # 商品ID
    send_user_id = models.ForeignKey('User', models.CASCADE, related_name='it_send_this_record')  # 发表用户ID
    recv_user_id = models.ForeignKey('User', models.CASCADE, related_name='it_recv_this_record')  # 接收用户ID
    content = models.CharField(max_length=256)  # 留言内容
    create_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "聊天记录"
        verbose_name_plural = "聊天记录"


class Follow(models.Model):
    id = models.AutoField(primary_key=True)  # 关注ID
    fans_user_id = models.ForeignKey('User', models.CASCADE, related_name='its_fans')  # 粉丝ID
    user_id = models.ForeignKey('User', models.CASCADE, related_name='it_love')  # 被关注者 ID
    create_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return "关注ID：" + str(self.id)

    class Meta:
        ordering = ["-create_at"]

        verbose_name = "关注者"
        verbose_name_plural = "关注者"


class Collection(models.Model):
    id = models.AutoField(primary_key=True)  # 收藏记录ID
    user_id = models.ForeignKey('User', models.CASCADE)  # 用户ID
    goods_id = models.ForeignKey('Goods', models.CASCADE)  # 商品ID
    create_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_at = models.DateTimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return "收藏记录ID：" + str(self.id)

    class Meta:
        ordering = ["-create_at"]
        verbose_name = "收藏记录"
        verbose_name_plural = "收藏记录"
