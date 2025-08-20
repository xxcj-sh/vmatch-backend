const ApiClient = require('./client');

class MatchingAPI extends ApiClient {
  // 获取匹配卡片
  async getMatchCards(matchType, userRole, page = 1, pageSize = 10) {
    // 只在明确测试模式下使用模拟数据
    const isTestMode = wx.getStorageSync('testMode') || false;
    
    if (isTestMode) {
      console.log('测试模式：使用模拟匹配卡片数据');
      return this.getMockMatchCards(matchType, userRole, page, pageSize);
    }
    
    // 生产模式：使用真实API
    console.log('生产模式：调用真实API获取匹配卡片');
    return this.request({
      url: `/cards/match?type=${matchType}&userRole=${userRole}&page=${page}&pageSize=${pageSize}`,
      method: 'GET'
    });
  }

  // 获取模拟匹配卡片数据（测试用）
  // 将原来的定义
  static async getMockMatchCards(matchType, userRole, page = 1, limit = 10) {
      // 模拟网络延迟
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // 获取当前用户信息（模拟租客身份）
      const currentUser = {
          id: 'tenant_001',
          name: '小明',
          avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face',
          age: 25,
          occupation: '软件工程师',
          role: 'seeker'
      };
      
      let mockData = [];
      
      switch (matchType) {
          case 'housing':
              // 房源匹配数据 - 从房东视角提供房源
              const housingLandlords = [
                  {
                      id: 'landlord_001',
                      name: '张女士',
                      avatar: 'https://images.unsplash.com/photo-1494790108755-2616b332-3fc9-4198-8d23-0f433b1f1b32?w=400&h=400&fit=crop&crop=face',
                      age: 32,
                      occupation: '产品经理',
                      distance: '500m',
                      interests: ['阅读', '瑜伽', '旅行'],
                      preferences: ['安静', '爱干净', '稳定工作'],
                      bio: '我是一个热爱生活的房东，希望找到一位爱干净的租客，一起维护温馨的小家。',
                      videoUrl: 'https://cdn.pixabay.com/video/2021/08/30/86867-594991237_tiny.mp4'
                  }
              ];
              
              const houseList = [
                  {
                      id: 'house_001',
                      title: '温馨一居室',
                      images: [
                          'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
                          'https://images.unsplash.com/photo-1560185127-6c93f25931ae?w=800&h=600&fit=crop',
                          'https://images.unsplash.com/photo-1560448205-4d9b3e6bb6db?w=800&h=600&fit=crop'
                      ],
                      price: 2800,
                      area: 45,
                      orientation: '南向',
                      floor: '12/28',
                      hasElevator: true,
                      decoration: '精装修',
                      community: '阳光小区',
                      location: '朝阳区',
                      deposit: '押一付三',
                      features: ['近地铁', '拎包入住', '家电齐全'],
                      videoUrl: 'https://cdn.pixabay.com/video/2024/08/25/228180_tiny.mp4'
                  },
                  {
                      id: 'house_002',
                      title: '现代两居室',
                      images: [
                          'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=600&fit=crop',
                          'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=600&fit=crop',
                          'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop'
                      ],
                      price: 4200,
                      area: 78,
                      orientation: '南北通透',
                      floor: '8/18',
                      hasElevator: true,
                      decoration: '简装修',
                      community: '绿城花园',
                      location: '海淀区',
                      deposit: '押一付二',
                      features: ['近商圈', '地铁沿线', '有车位'],
                      videoUrl: 'https://cdn.pixabay.com/video/2024/08/25/228181_tiny.mp4'
                  },
                  {
                      id: 'house_003',
                      title: 'loft复式公寓',
                      images: [
                          'https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&h=600&fit=crop',
                          'https://images.unsplash.com/photo-1540932239986-30128078f3c5?w=800&h=600&fit=crop',
                          'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&h=600&fit=crop'
                      ],
                      price: 3800,
                      area: 60,
                      orientation: '东向',
                      floor: '15/30',
                      hasElevator: true,
                      decoration: '精装修',
                      community: '星河湾',
                      location: '朝阳区',
                      deposit: '押一付三',
                      features: ['loft设计', '高层景观', '智能家居'],
                      videoUrl: 'https://cdn.pixabay.com/video/2024/08/25/228182_tiny.mp4'
                  }
              ];
              
              mockData = houseList.map((house, index) => ({
                  ...housingLandlords[index % housingLandlords.length],
                  houseInfo: house,
                  landlordInfo: housingLandlords[index % housingLandlords.length],
                  matchType: 'housing'
              }));
              break;
              
          case 'activity':
              // 活动匹配数据
              mockData = [
                  {
                      id: 'activity_001',
                      name: '周末爬山活动',
                      avatar: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop&crop=face',
                      age: 28,
                      occupation: '户外教练',
                      distance: '2km',
                      interests: ['户外运动', '摄影', '健康'],
                      activityName: '香山徒步一日游',
                      activityType: '户外运动',
                      activityTime: '周六 08:00-17:00',
                      activityLocation: '香山公园',
                      activityPrice: 88,
                      description: '一起爬山，享受大自然的美好，结交志同道合的朋友',
                      includes: ['专业领队', '保险', '摄影服务'],
                      matchType: 'activity',
                      videoUrl: 'https://cdn.pixabay.com/video/2021/08/27/86548-593924591_tiny.mp4'
                  }
              ];
              break;
              
          case 'dating':
                  // 约会匹配数据
                  mockData = [
                      {
                          id: 'dating_001',
                          name: '小雨',
                          avatar: 'https://images.unsplash.com/photo-1494790108755-2616b332-3fc9-4198-8d23-0f433b1f1b32?w=400&h=400&fit=crop&crop=face',
                          age: 26,
                          occupation: 'UI设计师',
                          distance: '800m',
                          interests: ['设计', '音乐', '旅行'],
                          height: 165,
                          education: '本科',
                          income: '15k-20k',
                          hobbies: ['画画', '看电影', '瑜伽'],
                          lookingFor: '真诚、有趣、有上进心的男生',
                          bio: '热爱生活，喜欢探索新事物的设计师小姐姐',
                          matchType: 'dating',
                          videoUrl: 'https://cdn.pixabay.com/video/2021/08/27/86548-593924591_tiny.mp4'
                      }
                  ];
                  break;
      }
      
      // 过滤掉当前用户自己的数据
      const filteredData = mockData.filter(item => item.id !== currentUser.id);
      
      // 分页处理
      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + limit;
      const paginatedData = filteredData.slice(startIndex, endIndex);
      
      return {
          list: paginatedData,
          total: filteredData.length,
          page,
          limit
      };
  }

  // 获取模拟匹配卡片数据（测试用）
  getMockMatchCards(matchType, userRole, page, pageSize) {
    let mockData = {
      list: [],
      total: 0,
      page: page,
      pageSize: pageSize
    };

    // 获取当前用户信息（租客）
    const currentUser = {
      id: 'current_user_001',
      name: '王思远',
      avatar: '/images/icon-user.png',
      age: 28,
      occupation: '高级前端工程师',
      company: '字节跳动'
    };

    // 根据匹配类型和用户角色生成对应的测试数据
    if (matchType === 'housing') {
      // 房东角色：显示租客资料
      if (userRole === 'provider') {
        mockData = {
          list: [
            {
              id: 'tenant_001',
              name: '王思远',
              avatar: '/images/icon-user.png',
              age: 28,
              occupation: '高级前端工程师',
              distance: '0.5km',
              interests: ['摄影', '徒步', '咖啡拉花', '独立音乐'],
              preferences: ['爱干净', '作息规律', '不抽烟', '无宠物'],
              bio: '字节跳动高级前端工程师，5年工作经验。喜欢摄影和户外活动，性格随和，作息规律，希望找到舒适安静的居住环境',
              matchType: matchType,
              userRole: 'seeker',
              // 租客信息
              tenantInfo: {
                budget: 4000,
                moveInDate: '2024-04-01',
                preferredAreas: ['望京', '朝阳', '海淀'],
                roomType: '一居室或两居室',
                leaseDuration: '一年以上',
                workLocation: '字节跳动总部',
                workType: '互联网',
                hasPet: false,
                smoking: false,
                drinking: '偶尔',
                cleanliness: '非常爱干净',
                socialLevel: '适中',
                cooking: '经常做饭'
              },
              contactInfo: {
                id: 'tenant_001',
                name: '王思远',
                avatar: '/images/icon-user.png',
                occupation: '高级前端工程师',
                verified: true,
                responseRate: '96%',
                joinDate: '2023-06-15',
                bio: '字节跳动高级前端工程师，性格随和，作息规律，希望找到舒适安静的居住环境'
              }
            }
          ],
          total: 1,
          page: page,
          pageSize: pageSize
        };
      } else {
        // 租客角色：显示房源信息（保持原有数据结构）
        mockData = {
          list: [
            {
              id: 'prop_001',
              name: 'CBD两居室',
              avatar: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
              age: 35,
              occupation: '互联网创业者',
              distance: '2.1km',
              interests: ['创业', '投资', '科技产品'],
              preferences: ['安静', '爱干净', '有稳定工作'],
              bio: '连续创业者，房源位于CBD核心区，希望找到注重生活品质的租客',
              matchType: matchType,
              userRole: 'provider',
              houseInfo: {
                image: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
                images: [
                  'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
                  'https://images.unsplash.com/photo-1560448204-61dc36dc98c8?w=800&h=600&fit=crop',
                  'https://images.unsplash.com/photo-1554995207-c18c203602cb?w=800&h=600&fit=crop'
                ],
                videoUrl: 'https://cdn.pixabay.com/video/2025/07/12/290859_tiny.mp4', // 视频优先展示
                videoUrl: 'https://cdn.pixabay.com/video/2025/07/12/290859_tiny.mp4',
                price: 6800,
                area: 65,
                orientation: '南北通透',
                floor: '20/28',
                hasElevator: true,
                decoration: '现代简约',
                community: '阳光上东',
                location: '朝阳区东三环北路8号',
                deposit: '押一付三',
                features: ['南北通透', '双阳台', '近地铁10号线', 'CBD核心']
              },
              landlordInfo: {
                id: 'landlord_002',
                name: '张伟明',
                avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop&crop=face',
                occupation: '互联网创业者',
                verified: true,
                responseRate: '95%',
                joinDate: '2020-05-10',
                bio: '连续创业者，目前经营一家互联网公司。为人直爽，好沟通，希望为租客提供舒适的居住体验。'
                }
                }, {
                  id: 'prop_002',
                  name: '五道口loft公寓',
                  avatar: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop',
                  age: 29,
                  occupation: 'UI设计师',
                  distance: '1.2km',
                  interests: ['设计', '艺术', '咖啡', '旅行'],
                  preferences: ['有创意', '性格开朗', '爱整洁'],
                  bio: '自由UI设计师，喜欢简约现代的设计风格，希望租客也有良好的审美品味',
                  matchType: matchType,
                  userRole: 'provider',
                  houseInfo: {
                    image: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop',
                    images: [
                      'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop',
                      'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=600&fit=crop',
                      'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=600&fit=crop'
                    ],
                    videoUrl: 'https://gossv-vcg.cfp.cn/videos/mts_videos/medium/VCG42N1328699212.mp4',
                    price: 4200,
                    area: 45,
                    orientation: '南向',
                    floor: '8/15',
                    hasElevator: true,
                    decoration: '北欧风格',
                    community: '华清嘉园',
                    location: '海淀区五道口',
                    deposit: '押一付一',
                    features: ['南向采光', 'loft设计', '近地铁13号线', '文艺氛围']
                  },
                  landlordInfo: {
                    id: 'landlord_003',
                    name: '李雨桐',
                    avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face',
                    occupation: 'UI设计师',
                    verified: true,
                    responseRate: '98%',
                    joinDate: '2021-03-20',
                    bio: '独立UI设计师，热爱艺术与设计，注重生活品质，希望与有趣的租客共享空间。'
                  }
                }
                ],
          total: 1,
          page: page,
          pageSize: pageSize
        };
      }
    } else if (matchType === 'activity') {
      mockData = {
        list: [
          {
            id: 'act_001',
            name: '古北水镇徒步摄影',
            avatar: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop&crop=face',
            age: 27,
            occupation: '户外摄影师',
            distance: '0.9km',
            interests: ['摄影', '登山', '露营', '星空摄影'],
            preferences: ['热爱自然', '体力好', '性格开朗'],
            bio: '专业户外摄影师，曾徒步川藏线、尼泊尔EBC。希望通过徒步活动认识更多热爱大自然的朋友',
            matchType: matchType,
            activityInfo: {
              image: 'https://images.unsplash.com/photo-1551632811-561732d1e95d?w=800&h=600&fit=crop',
              images: [
                'https://images.unsplash.com/photo-1551632811-561732d1e95d?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop'
              ],
              videoUrl: 'https://cdn.pixabay.com/video/2021/08/27/86548-593924591_tiny.mp4', // 视频优先展示
              name: '古北水镇徒步摄影',
              type: '户外徒步',
              date: '2024-03-16',
              time: '07:30-19:00',
              location: '密云古北水镇',
              price: 128,
              maxParticipants: 12,
              currentParticipants: 8,
              description: '专业摄影师带队，徒步古北水镇，拍摄长城日落和古镇夜景',
              includes: ['专业指导', '摄影技巧分享', '交通接送', '保险']
            },
            organizerInfo: {
              id: 'organizer_001',
              name: '刘思琪',
              avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&h=400&fit=crop&crop=face',
              occupation: '户外摄影师',
              verified: true,
              experience: '5年专业摄影经验',
              bio: '专业户外摄影师，曾徒步川藏线、尼泊尔EBC'
            }
          }
        ],
        total: 1,
        page: page,
        pageSize: pageSize
      };
    } else if (matchType === 'dating') {
      mockData = {
        list: [
          {
            id: 'dating_001',
            name: '李小雨',
            avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop&crop=face',
            age: 26,
            occupation: 'UI设计师',
            distance: '0.7km',
            interests: ['设计', '咖啡', '旅行', '瑜伽'],
            preferences: ['有品味', '幽默', '上进'],
            bio: '温柔善良的UI设计师，喜欢美好的事物，期待一场真诚的相遇',
            matchType: matchType,
            gender: 'female',
            height: 165,
            education: '硕士',
            income: '10k-15k',
            hobbies: ['绘画', '钢琴', '烘焙', '瑜伽'],
            lookingFor: '成熟稳重、有责任心的男生',
            videoUrl: 'https://cdn.pixabay.com/video/2021/08/27/86548-593924591_tiny.mp4' // 视频优先展示
          }
        ],
        total: 1,
        page: page,
        pageSize: pageSize
      };
    }
    
    // 模拟网络延迟
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(mockData);
      }, 500);
    });
  }

  // 获取匹配列表（matches页面使用）
  async getMatches(status = null) {
    // 测试模式：返回模拟匹配数据
    console.log('测试模式：使用模拟匹配列表数据');
    return this.getMockMatches(status);
  }

  // 获取模拟匹配数据（matches页面测试用）
  getMockMatches(status = null) {
    // 测试模式下从本地存储获取真实的测试匹配记录
    const savedMatches = wx.getStorageSync('testMatches') || [];
    
    // 根据状态过滤匹配
    let filteredMatches = savedMatches;
    if (status === 'new') {
      filteredMatches = savedMatches.filter(m => !m.isRead);
    } else if (status === 'contacted') {
      filteredMatches = savedMatches.filter(m => m.isRead);
    }
    
    const mockMatches = {
      list: filteredMatches,
      total: filteredMatches.length,
      page: 1,
      pageSize: 10
    };

    // 模拟网络延迟
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(mockMatches);
      }, 300);
    });
  }

  // 清理测试匹配数据
  clearTestMatches() {
    wx.removeStorageSync('testMatches');
    console.log('已清理所有测试匹配记录');
  }

  // 提交匹配操作
  async submitMatchAction(cardId, action, matchType) {
    try {
      const data = await this.request({
        url: '/match/action',
        method: 'POST',
        data: {
          cardId,
          action,
          matchType
        }
      });
      
      return data;
    } catch (error) {
      console.error('提交匹配操作失败:', error);
      throw error;
    }
  }

  // 滑动卡片操作
  async swipeCard(cardId, direction) {
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：模拟滑动操作', { cardId, direction });
      
      // 左滑明确不会触发匹配，只有右滑和上滑可能触发
      if (direction === 'left') {
        console.log('左滑操作：跳过卡片，不会触发匹配');
        return {
          isMatch: false
        };
      }
      
      // 右滑和上滑有30%概率匹配成功
      const isMatch = Math.random() < 0.8;
      return {
        isMatch: isMatch
      };
    }

    try {
      const data = await this.request({
        url: '/match/swipe',
        method: 'POST',
        data: {
          cardId,
          direction
        }
      });
      
      return data;
    } catch (error) {
      console.error('滑动操作失败:', error);
      throw error;
    }
  }

  // 获取匹配详情
  async getMatchDetail(matchId) {
    if (wx.getStorageSync('testMode')) {
      console.log('测试模式：获取匹配详情', matchId);
      
      // 从getMockMatches获取一致的数据
      const mockData = await this.getMockMatches();
      const match = mockData.list.find(m => m.id === parseInt(matchId));
      
      if (match) {
        return {
          id: match.id,
          name: match.name,
          avatar: match.avatar,
          age: match.age || 25,
          location: match.location,
          occupation: match.occupation || '未知',
          education: match.education || '未知',
          height: match.height || '未知',
          reason: match.reason || '你们很有默契！'
        };
      }
      
      // 回退数据
      return {
        id: matchId,
        name: '测试用户',
        avatar: '../../images/profile.png',
        age: 25,
        location: '北京',
        occupation: '测试职业',
        education: '本科',
        height: 170,
        reason: '测试匹配原因'
      };
    }

    try {
      const data = await this.request({
        url: `/match/detail/${matchId}`,
        method: 'GET'
      });
      
      return data;
    } catch (error) {
      console.error('获取匹配详情失败:', error);
      throw error;
    }
  }

  // 获取匹配列表
  async getMatchList(page = 1, pageSize = 10, status = 'all') {
    try {
      const data = await this.request({
        url: '/match/list',
        method: 'GET',
        data: {
          page,
          pageSize,
          status
        }
      });
      
      return data;
    } catch (error) {
      console.error('获取匹配列表失败:', error);
      throw error;
    }
  }
}

module.exports = MatchingAPI;