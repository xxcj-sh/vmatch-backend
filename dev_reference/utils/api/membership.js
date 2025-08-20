const ApiClient = require('./client');

class MembershipAPI extends ApiClient {
  // 获取会员信息
  async getMembershipInfo() {
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：获取模拟会员信息');
      
      // 返回测试用的会员信息
      return {
        level: 'premium',
        levelName: '高级会员',
        expireDate: '2025-12-31',
        features: [
          '无限次滑动',
          '查看谁喜欢了你',
          '高级筛选功能',
          '专属客服'
        ],
        remainingSwipes: 999,
        totalSwipes: 999
      };
    }

    try {
      const data = await this.request({
        url: '/membership/info',
        method: 'GET'
      });
      
      return data;
    } catch (error) {
      console.error('获取会员信息失败:', error);
      throw error;
    }
  }

  // 创建会员支付
  async createMembershipPayment(planId) {
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：创建模拟会员支付', planId);
      
      // 模拟支付成功
      return {
        orderId: 'test_order_' + Date.now(),
        amount: 19.9,
        status: 'pending',
        paymentUrl: 'https://example.com/payment/test'
      };
    }

    try {
      const data = await this.request({
        url: '/membership/payment',
        method: 'POST',
        data: {
          planId
        }
      });
      
      return data;
    } catch (error) {
      console.error('创建会员支付失败:', error);
      throw error;
    }
  }
}

module.exports = MembershipAPI;