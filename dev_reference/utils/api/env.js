// 环境配置
const ENV_CONFIG = {
  // 开发环境
  development: {
    baseURL: 'http://localhost:8000/api/v1',
    envName: 'development'
  },
  
  // 测试环境
  testing: {
    baseURL: 'http://test.api.wematch.example.com/api/v1',
    envName: 'testing'
  },
  
  // 生产环境
  production: {
    baseURL: 'https://api.wematch.example.com/api/v1',
    envName: 'production'
  }
};

// 获取当前环境
function getCurrentEnv() {
  // 测试模式
  if (wx.getStorageSync('testMode')) {
    return 'testing';
  }
  
  // 根据小程序的环境变量判断
  // #ifdef MP-WEIXIN
  const info = wx.getAccountInfoSync();
  if (info.miniProgram.envVersion === 'develop') {
    return 'development';
  } else if (info.miniProgram.envVersion === 'trial') {
    return 'testing';
  } else {
    return 'production';
  }
  // #endif
  
  // 默认返回开发环境
  return 'development';
}

// 获取当前环境配置
function getCurrentEnvConfig() {
  const env = getCurrentEnv();
  return ENV_CONFIG[env] || ENV_CONFIG.development;
}

module.exports = {
  getCurrentEnv,
  getCurrentEnvConfig
};