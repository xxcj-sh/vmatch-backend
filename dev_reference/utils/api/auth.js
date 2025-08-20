const ApiClient = require('./client');
const { STORAGE_KEYS } = require('./config');

class AuthAPI extends ApiClient {
  // 微信登录
  async wxLogin(code, userInfo = null) {
    // 测试模式：跳过实际微信登录
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：跳过微信登录');
      return {
        token: 'test_token_123456',
        expiresIn: 7200,
        userInfo: {
          id: 1,
          nickname: '测试用户',
          avatar: '/images/icon-user.png',
          gender: 1,
          age: 25
        }
      };
    }
    
    try {
      const data = await this.request({
        url: '/auth/login',
        method: 'POST',
        data: {
          code: code,
          userInfo: userInfo
        },
        needAuth: false
      });

      // 保存token
      this.setToken(data.token, data.expiresIn);
      
      // 保存用户信息
      console.log('保存用户信息前检查:', {data: data, STORAGE_KEYS: STORAGE_KEYS});
      if (!STORAGE_KEYS) {
        console.error('STORAGE_KEYS未定义');
      } else if (!STORAGE_KEYS.USER_INFO) {
        console.error('STORAGE_KEYS.USER_INFO未定义');
      } else if (!data) {
        console.error('data未定义');
      } else if (!data.userInfo) {
        console.error('data.userInfo未定义');
      } else {
        wx.setStorageSync(STORAGE_KEYS.USER_INFO, data.userInfo);
      }
      
      return data;
    } catch (error) {
      console.error('微信登录失败:', error);
      throw error;
    }
  }

  // 手机号登录
  async loginWithPhone(phone, code) {
    try {
      const data = await this.request({
        url: '/auth/login/phone',
        method: 'POST',
        data: { phone, code },
        needAuth: false
      });

      this.setToken(data.token, data.expiresIn);
      return data;
    } catch (error) {
      console.error('手机号登录失败:', error);
      throw error;
    }
  }

  // 发送验证码
  async sendVerificationCode(phone) {
    try {
      const data = await this.request({
        url: '/auth/sms-code',
        method: 'POST',
        data: { phone },
        needAuth: false
      });
      return data;
    } catch (error) {
      console.error('发送验证码失败:', error);
      throw error;
    }
  }

  // 微信登录
  async loginWithWeChat(code) {
    try {
      const data = await this.request({
        url: '/auth/login/wechat',
        method: 'POST',
        data: { code },
        needAuth: false
      });

      this.setToken(data.token, data.expiresIn);
      return data;
    } catch (error) {
      console.error('微信登录失败:', error);
      throw error;
    }
  }

  // 注册新用户
  async registerUser(userData) {
    try {
      const data = await this.request({
        url: '/auth/register',
        method: 'POST',
        data: userData,
        needAuth: false
      });

      this.setToken(data.token, data.expiresIn);
      return data;
    } catch (error) {
      console.error('用户注册失败:', error);
      throw error;
    }
  }

  // 退出登录
  async logout() {
    // 测试模式：模拟退出成功
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：退出登录成功');
      return { success: true };
    }

    try {
      const data = await this.request({
        url: '/auth/logout',
        method: 'POST'
      });
      
      return data;
    } catch (error) {
      console.error('退出登录失败:', error);
      throw error;
    }
  }

  // 验证token
  async validateToken() {
    try {
      await this.request({
        url: '/auth/validate',
        method: 'GET'
      });
      return true;
    } catch (error) {
      return false;
    }
  }

  // 手机号登录（兼容旧方法名）
  async phoneLogin(phone, code) {
    return this.loginWithPhone(phone, code);
  }

  // 手机号登录（兼容旧方法名）
  async phoneLogin(phone, code) {
    return this.loginWithPhone(phone, code);
  }

  // 发送验证码（兼容旧方法名）
  async sendVerificationCode(phone) {
    return this.sendVerificationCode(phone);
  }

  // 注册（兼容旧方法名）
  async register(userData) {
    return this.registerUser(userData);
  }

  // 上传图片
  async uploadImage(filePath) {
    try {
      const data = await this.request({
        url: '/upload/image',
        method: 'POST',
        data: { filePath },
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return data;
    } catch (error) {
      console.error('上传图片失败:', error);
      throw error;
    }
  }
}

module.exports = AuthAPI;