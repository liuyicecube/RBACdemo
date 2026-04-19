<template>
  <div class="not-found-page">
    <div class="content">
      <h1 class="code">404</h1>
      <p class="message">页面不存在</p>
      <p class="description">抱歉，您访问的页面不存在</p>
      <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped lang="scss">
.not-found-page {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;

  .content {
    text-align: center;

    .code {
      font-size: 120px;
      color: #909399;
      line-height: 1;
      margin-bottom: 20px;
    }

    .message {
      font-size: 24px;
      color: #606266;
      margin-bottom: 10px;
    }

    .description {
      font-size: 14px;
      color: #909399;
      margin-bottom: 30px;
    }
  }
}
</style>
