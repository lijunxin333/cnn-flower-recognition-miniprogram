// utils\request.js
const { BASE_URL } = require("./config");

// 上传图片
function uploadImage(filePath) {
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: BASE_URL + "/predict",
      filePath: filePath,
      name: "image",

      success(res) {
        console.log("后端返回：", res.data);
        resolve(JSON.parse(res.data));
      },

      fail(err) {
        console.log("上传失败：", err);
        reject(err);
      }
    });
  });
}

// 收藏花卉
function addFavorite(user_id, flower_id) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: BASE_URL + "/favorite/add",
      method: "POST",
      data: {
        user_id,
        flower_id
      },
      success(res) {
        resolve(res.data);
      },
      fail(err) {
        reject(err);
      }
    });
  });
}

// 获取收藏列表
function getFavoriteList(user_id) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: BASE_URL + "/favorite/list?user_id=" + user_id,
      method: "GET",
      success(res) {
        resolve(res.data);
      },
      fail(err) {
        reject(err);
      }
    });
  });
}

// 返回花卉详细信息
function getFlowerDetail(id) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: BASE_URL + "/flower/detail?id=" + id,
      method: "GET",
      success(res) {
        resolve(res.data);
      },
      fail(err) {
        reject(err);
      }
    });
  });
}

module.exports = {
  uploadImage,
  getFlowerDetail,
  addFavorite,
  getFavoriteList,
  BASE_URL
};