class Vector3D:
    def __init__(self, x, y, z):
        # 定义私有数据成员 (以双下划线开头)
        self.__x = x
        self.__y = y
        self.__z = z

    def __add__(self, other):
        """重载 + 运算符：向量加法"""
        return Vector3D(self.__x + other.__x, self.__y + other.__y, self.__z + other.__z)

    def __sub__(self, other):
        """重载 - 运算符：向量减法"""
        return Vector3D(self.__x - other.__x, self.__y - other.__y, self.__z - other.__z)

    def __mul__(self, scalar):
        """重载 * 运算符：向量与标量乘法"""
        return Vector3D(self.__x * scalar, self.__y * scalar, self.__z * scalar)

    def __truediv__(self, scalar):
        """重载 / 运算符：向量与标量除法"""
        if scalar == 0:
            raise ValueError("除数不能为 0")
        return Vector3D(self.__x / scalar, self.__y / scalar, self.__z / scalar)

    @property
    def length(self):
        """使用 property 将方法伪装成属性：计算向量长度"""
        return (self.__x**2 + self.__y**2 + self.__z**2) ** 0.5

    def __str__(self):
        """控制 print() 输出的格式"""
        return f"({self.__x}, {self.__y}, {self.__z})"

if __name__ == "__main__":
    try:
        print("=== 三维向量类测试 ===")
        x1, y1, z1 = map(float, input("请输入向量 v1 的三个坐标(用空格分隔): ").split())
        v1 = Vector3D(x1, y1, z1)
        
        x2, y2, z2 = map(float, input("请输入向量 v2 的三个坐标(用空格分隔): ").split())
        v2 = Vector3D(x2, y2, z2)
        
        scalar = float(input("请输入一个用于乘除的标量(数字): "))
        
        print("\n--- 计算结果 ---")
        print(f"v1 状态: {v1}, 长度: {v1.length:.2f}")
        print(f"v2 状态: {v2}, 长度: {v2.length:.2f}")
        print(f"v1 + v2 = {v1 + v2}")
        print(f"v1 - v2 = {v1 - v2}")
        print(f"v1 * {scalar} = {v1 * scalar}")
        print(f"v1 / {scalar} = {v1 / scalar}")
        
    except ValueError as e:
        print(f"输入错误: 请确保输入的是有效的数字。详细信息: {e}")