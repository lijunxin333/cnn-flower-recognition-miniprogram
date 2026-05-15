// pages/profile/profile.js
const { getFavoriteList } = require("../../utils/request");
const { BASE_URL } = require("../../utils/config");

Page({
  data: {
    username: "",
    userId: "",
    favoriteCount: 0
  },

  onShow() {
    this.loadUserInfo();
    this.loadFavorite();
  },

  // 加载用户信息
  loadUserInfo() {
    const userId = wx.getStorageSync("user_id");
    const username = wx.getStorageSync("username");

    this.setData({
      userId,
      username
    });
  },

  // 加载收藏数量
  async loadFavorite() {
    const userId = wx.getStorageSync("user_id");

    if (!userId) return;

    try {
      const res = await getFavoriteList(userId);

      const list = res.data || [];

      this.setData({
        favoriteCount: list.length
      });

    } catch (e) {
      console.log("获取收藏失败", e);
    }
  },

  // 退出登录
  logout() {
    wx.showModal({
      title: "提示",
      content: "确定要退出登录吗？",
      success: (res) => {
        if (res.confirm) {

          // 清除缓存
          wx.clearStorageSync();

          wx.showToast({
            title: "已退出"
          });

          setTimeout(() => {
            wx.redirectTo({
              url: "/pages/login/login"
            });
          }, 500);
        }
      }
    });
  }
});