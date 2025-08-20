const ApiClient = require('./client');
const { STORAGE_KEYS } = require('./config');

class UserAPI extends ApiClient {
  // 获取用户信息
  async getUserInfo() {
    // 测试模式：返回模拟用户信息
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：使用模拟用户信息');
      const mockUserInfo = {
        id: 1,
        nickname: '测试用户',
        avatar: '/images/icon-user.png',
        gender: 1,
        age: 25,
        matchType: 'housing',
        userRole: 'seeker'
      };
      console.log('测试模式保存用户信息前检查:', {STORAGE_KEYS: STORAGE_KEYS, mockUserInfo: mockUserInfo});
      if (!STORAGE_KEYS) {
        console.error('STORAGE_KEYS未定义');
      } else if (!STORAGE_KEYS.USER_INFO) {
        console.error('STORAGE_KEYS.USER_INFO未定义');
      } else {
        wx.setStorageSync(STORAGE_KEYS.USER_INFO, mockUserInfo);
      }
      return mockUserInfo;
    }
    
    try {
      const data = await this.request({
        url: '/user/info',
        method: 'GET'
      });

      const userData = data.data.data;
      // 更新本地存储
      console.log('API返回后保存用户信息前检查:', {STORAGE_KEYS: STORAGE_KEYS, data: userData});
      if (!STORAGE_KEYS) {
        console.error('STORAGE_KEYS未定义');
      } else if (!STORAGE_KEYS.USER_INFO) {
        console.error('STORAGE_KEYS.USER_INFO未定义');
      } else if (!userData) {
        console.error('userData未定义');
      } else {
        wx.setStorageSync(STORAGE_KEYS.USER_INFO, userData);
      }
      
      return userData;
    } catch (error) {
      console.error('获取用户信息失败:', error);
      throw error;
    }
  }

  // 获取个人资料
  async getProfile() {
    try {
      const data = await this.request({
        url: '/profile/get',
        method: 'GET'
      });
      
      return data;
    } catch (error) {
      console.error('获取个人资料失败:', error);
      throw error;
    }
  }

  // 获取其他用户资料
  async getOtherUserProfile(userId) {
    // 测试模式：返回模拟数据
    if (wx.getStorageSync('testMode')) {
      console.log('API: 获取他人用户资料，userId:', userId);
      
      // 根据不同的userId返回不同的模拟数据，使测试更真实
      const mockProfiles = {
        'landlord_001': {
          id: 'landlord_001',
          nickname: '林晓燕',
          avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop&crop=face',
          age: 32,
          gender: 'female',
          location: '北京',
          occupation: '房产投资顾问',
          education: '硕士',
          height: 165,
          bio: '专业房产顾问，在北京有多套优质房源。为人随和，好沟通，希望能为租客提供舒适的居住体验。',
          photos: [
            { url: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop&crop=face', type: 'avatar' },
            { url: 'https://images.unsplash.com/photo-1522708323590-d2db1a6ee4ea?w=800&h=600&fit=crop', type: 'life' },
            { url: 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop', type: 'life' }
          ],
          interests: ['房产投资', '室内设计', '智能家居'],
          role: 'landlord',
          tags: ['随和', '有责任感', '爱干净']
        }
      };
      
      const profile = mockProfiles[userId] || {
        id: userId,
        nickname: `用户${userId.slice(-4)}`,
        avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=400&h=400&fit=crop&crop=face',
        age: 26,
        gender: 'male',
        location: '北京',
        occupation: '软件工程师',
        education: '本科',
        height: 175,
        bio: '暂无个人简介',
        photos: [
          { url: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=400&h=400&fit=crop&crop=face', type: 'avatar' }
        ],
        interests: ['阅读', '旅行'],
        role: 'seeker',
        tags: ['友好', '开朗']
      };
      
      console.log('API: 返回用户资料', {
        userId: profile.id,
        nickname: profile.nickname,
        avatar: profile.avatar
      });
      
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(profile);
        }, 500);
      });
    }
    
    try {
      // 使用API获取指定用户的资料
      const data = await this.request({
        url: `/user/profile/${userId}`,
        method: 'GET'
      });
      
      return data;
    } catch (error) {
      console.error('获取他人用户资料失败:', error);
      
      // 如果特定接口不存在，尝试使用通用接口
      try {
        const data = await this.request({
          url: `/profile/get/${userId}`,
          method: 'GET'
        });
        
        return data;
      } catch (fallbackError) {
        console.error('备用接口也失败:', fallbackError);
        throw fallbackError;
      }
    }
  }

  // 更新个人资料
  async updateProfile(profileData) {
    try {
      const data = await this.request({
        url: '/profile/update',
        method: 'POST',
        data: profileData
      });
      
      return data;
    } catch (error) {
      console.error('更新个人资料失败:', error);
      throw error;
    }
  }

  // 获取用户完整资料（个人中心用）
  async getUserProfile() {
    // 测试模式：返回模拟的用户资料
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：使用模拟用户资料');
      return {
        id: 1,
        nickname: '王思远',
        avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face',
        phone: '138****5678',
        email: 'wang.siyuan@email.com',
        currentRole: 'tenant',
        roles: [
          { type: 'tenant', name: '租客' },
          { type: 'landlord', name: '房东' }
        ],
        bio: '字节跳动高级前端工程师，5年工作经验。喜欢摄影和户外活动，性格随和，作息规律。',
        interests: ['摄影', '徒步', '咖啡拉花', '独立音乐'],
        location: '北京',
        joinDate: '2023-06-15',
        verified: true
      };
    }

    try {
      const data = await this.request({
        url: '/user/profile',
        method: 'GET'
      });
      
      return data;
    } catch (error) {
      console.error('获取用户资料失败:', error);
      throw error;
    }
  }

  // 更新用户资料
  async updateUserProfile(profileData) {
    // 测试模式：模拟更新成功
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：更新用户资料成功', profileData);
      return { success: true };
    }

    try {
      const data = await this.request({
        url: '/user/profile',
        method: 'PUT',
        data: profileData
      });
      
      return data;
    } catch (error) {
      console.error('更新用户资料失败:', error);
      throw error;
    }
  }

  // 获取用户统计数据
  async getUserStats() {
    // 测试模式：返回模拟统计数据
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：使用模拟统计数据');
      return {
        matchCount: 12,
        messageCount: 45,
        favoriteCount: 8
      };
    }

    try {
      const data = await this.request({
        url: '/user/stats',
        method: 'GET'
      });
      
      return data;
    } catch (error) {
      console.error('获取用户统计数据失败:', error);
      throw error;
    }
  }

  // 获取个人资料（兼容旧方法名）
  async getProfile() {
    return this.getUserProfile();
  }

  // 更新个人资料（兼容旧方法名）
  async updateProfile(profileData) {
    return this.updateUserProfile(profileData);
  }

  // 获取用户完整资料（兼容旧方法名）
  async getUserFullProfile() {
    return this.getUserProfile();
  }
}

module.exports = UserAPI;