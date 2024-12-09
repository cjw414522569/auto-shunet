# auto-shunet
上海大学校园网自动化认证docker版

主要用于软路由openwrt下的docker环境
使用教程：
打开openwrt终端
cd /opt
git clone https://github.com/cjw414522569/auto-shunet.git
docker build -t auto-shunet .
docker run -d --privileged --name auto-shunet auto-shunet

高阶玩法：
用openwrt进行多拨，创建wan1,wan2,wan3接口，并且进行负载均衡，创建几个wan网速就可以翻几倍
去docker创建网络，驱动选择Mac vlan，基于设备wan1接口，模式选择专用，不创建创建 macvlan 接口
这样就可以分别去自动认证每个接口了
docker run -d --privileged --name auto-shunet --network wan1 auto-shunet
docker run -d --privileged --name auto-shunet --network wan2 auto-shunet
docker run -d --privileged --name auto-shunet --network wan3 auto-shunet
