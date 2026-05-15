// pages/home/home.js
const { uploadImage } = require("../../utils/request");
const { BASE_URL } = require("../../utils/config");


Page({
  data: {
    imagePath: ""
  },
  onShow() {
    const userId = wx.getStorageSync("user_id");
  
    if (!userId) {
      wx.redirectTo({
        url: "/pages/login/login"
      });
    }
  },

  chooseImage() {
    wx.chooseImage({
      count: 1,
      sizeType: ["compressed"],
      sourceType: ["album", "camera"],
      success: async (res) => {
        const path = res.tempFilePaths[0];

        this.setData({
          imagePath: path
        });

        wx.showLoading({
          title: "识别中..."
        });

        try {
          const result = await uploadImage(path);
          if (!result || !result.success) {
            wx.showToast({
              title: "识别失败",
              icon: "none"
            });
            return;
          }
          wx.hideLoading();

          wx.navigateTo({
            url: "/pages/result/result",
            success: (nav) => {
              nav.eventChannel.emit("resultData", result);
            }
          });

        } catch (e) {
          wx.hideLoading();
          wx.showToast({
            title: "识别失败",
            icon: "none"
          });
        }
      }
    });
  }
});
