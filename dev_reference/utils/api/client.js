const { API_CONFIG, STORAGE_KEYS } = require('./config');

class ApiClient {
  constructor() {
    this.baseURL = API_CONFIG.baseURL;
    this.timeout = API_CONFIG.timeout;
    this.retryCount = API_CONFIG.retryCount;
  }

  // 获取token
  getToken() {
    return wx.getStorageSync(STORAGE_KEYS.TOKEN);
  }

  // 设置token
  setToken(token, expiresIn) {
    wx.setStorageSync(STORAGE_KEYS.TOKEN, token);
    wx.setStorageSync(STORAGE_KEYS.EXPIRES_IN, Date.now() + expiresIn * 1000);
  }

  // 清除token
  clearToken() {
    wx.removeStorageSync(STORAGE_KEYS.TOKEN);
    wx.removeStorageSync(STORAGE_KEYS.EXPIRES_IN);
    wx.removeStorageSync(STORAGE_KEYS.USER_INFO);
  }

  // 检查token是否有效
  isTokenValid() {
    const expiresIn = wx.getStorageSync(STORAGE_KEYS.EXPIRES_IN);
    return expiresIn && Date.now() < expiresIn;
  }

  // 统一的请求方法
  async request(options) {
    const { url, method = 'GET', data = {}, headers = {}, needAuth = true } = options;
    
    // 测试模式：跳过实际网络请求
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：跳过网络请求', url);
      // 返回模拟的成功响应
      return {
        code: 0,
        message: '测试模式成功',
        data: {}
      };
    }
    
    // 构建完整URL
    const fullUrl = this.baseURL + url;
    
    // 构建请求头
    const requestHeaders = {
      'Content-Type': 'application/json',
      ...headers
    };
    
    // 如果需要认证，添加token
    if (needAuth) {
      const token = this.getToken();
      if (token) {
        requestHeaders['Authorization'] = `Bearer ${token}`;
      }
    }

    try {
      const response = await new Promise((resolve, reject) => {
        wx.request({
          url: fullUrl,
          method: method,
          data: data,
          header: requestHeaders,
          timeout: this.timeout,
          success: (res) => {
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve(res.data);
            } else {
              reject(new Error(`HTTP ${res.statusCode}: ${res.data?.message || '请求失败'}`));
            }
          },
          fail: (error) => {
            reject(new Error(`网络错误: ${error.errMsg}`));
          }
        });
      });

      // 检查业务逻辑错误
      if (response.code !== 0) {
        if (response.code === 401) {
          // token过期，清除本地token并重新登录
          this.clearToken();
          wx.showToast({
            title: '登录已过期，请重新登录',
            icon: 'none'
          });
          // 触发重新登录
          this.goToLogin();
        }
        throw new Error(response.message || '请求失败');
      }

      return response.data;
    } catch (error) {
      console.error('API请求失败:', error);
      throw error;
    }
  }

  // 跳转到登录页面
  goToLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    });
  }
}

module.exports = ApiClient;