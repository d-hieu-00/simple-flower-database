<template>
  <div class="card shadow inherit-height">
    <div class="card-header">
      <p class="fw-semibold pt-3 ps-3">Flower database - Cơ sở dữ liệu về loài hoa</p>
    </div>
    <div class="card-body">
      <div class="container ms-3 p-0">
        <p>Gồm 102 loài hoa khác nhau có thể dự đoán</p>
        <p>Với dataset ban đầu gồm ~8000 bức ảnh</p>
        <p>Hệ thống cho phép</p>
        <ul>
          <li>Tìm kiếm các loài hoa qua tên hoặc hình ảnh</li>
          <li>Thêm các hình ảnh mới vào cở sở dữ liệu</li>
          <li>Xóa các hình ảnh có trong cở sở dữ liệu</li>
        </ul>
        <br>
        <p>Dataset: <a class="link-primary" href="https://www.tensorflow.org/datasets/catalog/oxford_flowers102">
          https://www.tensorflow.org/datasets/catalog/oxford_flowers102</a>
        </p>
        <p>Pre-Trained Model: <a class="link-primary" href="https://github.com/openai/CLIP">CLIP Model</a>
        </p>
      </div>
    </div>
  </div>
</template>
