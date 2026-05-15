const { BASE_URL } = require("../../utils/config");

Page({
  data: {
    list: []
  },

  onShow() {
    const user_id = wx.getStorageSync("user_id");

    wx.request({
      url: BASE_URL + "/favorite/list",
      method: "GET",
      data: {
        user_id: user_id
      },

      success: (res) => {
        console.log("后端返回：", res.data);

        const data = (res.data && res.data.data) ? res.data.data : [];

        const list = data.map(item => ({
          ...item,
          img: BASE_URL + item.image_path   // ⭐ 注意字段统一
        }));

        this.setData({ list });
      }
    });
  },

  deleteItem(e) {
    const flower_id = Number(e.currentTarget.dataset.id);
    const user_id = wx.getStorageSync("user_id");
  
    wx.showModal({
      title: "提示",
      content: "确定要删除该收藏吗？",
      success: (res) => {
        if (res.confirm) {
  
          wx.request({
            url: BASE_URL + "/favorite/delete",
            method: "POST",
            data: {
              user_id,
              flower_id
            },
  
            success: (res) => {
              if (res.data.code === 0) {
  
                wx.showToast({ title: "删除成功" });
  
                const newList = this.data.list.filter(
                  item => item.id !== flower_id
                );
  
                this.setData({
                  list: newList
                });
  
              } else {
                wx.showToast({
                  title: "删除失败",
                  icon: "none"
                });
              }
            },
  
            fail: () => {
              wx.showToast({
                title: "网络错误",
                icon: "none"
              });
            }
          });
  
        }
      }
    });
  },

  goDetail(e) {
    const item = e.currentTarget.dataset.item;
    wx.navigateTo({
      url: "/pages/detail/detail",
      success: (res) => {
        res.eventChannel.emit("detailData", item);
      }
    });
  }
});