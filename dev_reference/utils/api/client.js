const { API_CONFIG, STORAGE_KEYS } = require('./config');
const { getCurrentEnvConfig } = require('./env');

class ApiClient {
  constructor() {
    this.timeout = API_CONFIG.timeout;
    this.retryCount = API_CONFIG.retryCount;
  }
  
  // 获取当前baseURL
  getBaseURL() {
    const envConfig = getCurrentEnvConfig();
    return envConfig.baseURL;
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
    console.log('清除token前检查:', {STORAGE_KEYS: STORAGE_KEYS});
    if (!STORAGE_KEYS) {
      console.error('STORAGE_KEYS未定义');
    } else {
      wx.removeStorageSync(STORAGE_KEYS.TOKEN);
      wx.removeStorageSync(STORAGE_KEYS.EXPIRES_IN);
      if (STORAGE_KEYS.USER_INFO) {
        wx.removeStorageSync(STORAGE_KEYS.USER_INFO);
      } else {
        console.error('STORAGE_KEYS.USER_INFO未定义');
      }
    }
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
    
    // 获取当前环境配置
    const envConfig = getCurrentEnvConfig();
    
    // 构建完整URL
    const fullUrl = this.getBaseURL() + url;
    
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

    // 记录请求信息
    console.log('API请求:', {
      url: fullUrl,
      method,
      env: envConfig.envName,
      baseURL: this.getBaseURL()
    });

    try {
      const response = await new Promise((resolve, reject) => {
        wx.request({
          url: fullUrl,
          method: method,
          data: data,
          header: requestHeaders,
          timeout: this.timeout,
          success: (res) => {
            console.log('API响应:', {
              url: fullUrl,
              statusCode: res.statusCode,
              data: res.data
            });
            
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve(res.data);
            } else {
              reject(new Error(`HTTP ${res.statusCode}: ${res.data?.message || '请求失败'}`));
            }
          },
          fail: (error) => {
            console.error('API请求失败:', {
              url: fullUrl,
              error: error.errMsg,
              env: envConfig.envName
            });
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

      // 返回响应数据，兼容不同的数据结构
      return {
        code: response.code || 0,
        message: response.message || 'success',
        data: response.data || response,
        success: response.code === 0
      };
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