// pages/login/login.js
const { BASE_URL } = require("../../utils/config");

Page({
  data: {
    username: "",
    password: ""
  },

  onUsernameInput(e) {
    this.setData({
      username: e.detail.value
    });
  },

  onPasswordInput(e) {
    this.setData({
      password: e.detail.value
    });
  },

  async handleLogin() {
    const { username, password } = this.data;

    if (!username || !password) {
      wx.showToast({
        title: "请输入完整信息",
        icon: "none"
      });
      return;
    }

    wx.showLoading({ title: "登录中..." });

    wx.request({
      url: BASE_URL + "/user/login",
      method: "POST",
      data: {
        username,
        password
      },
      success: (res) => {
        wx.hideLoading();
      
        const data = res.data;
      
        // ❗用 code 判断，不是 success
        if (data.code === 0) {
      
          const user = data.data;
      
          wx.setStorageSync("user_id", user.user_id);
          wx.setStorageSync("username", user.username);
      
          wx.showToast({
            title: "登录成功",
            icon: "success"
          });
      
          setTimeout(() => {
            wx.switchTab({
              url: "/pages/home/home"
            });
          }, 500);
      
        } else {
          wx.showToast({
            title: data.msg || "登录失败",
            icon: "none"
          });
        }
      },
      
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: "网络错误",
          icon: "none"
        });
      }
    });
  },

  goRegister() {
    wx.navigateTo({
      url: "/pages/register/register"
    });
  }
});