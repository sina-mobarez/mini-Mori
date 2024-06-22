<script>
export default {
  data() {
    return {
      searchTerm: "",
    };
  },
  methods: {
    updateSearch() {
      this.$emit("search-updated", this.searchTerm);
    },
    clearSearch() {
      this.searchTerm = "";
      this.updateSearch();
    },
  },
};
</script>

<template>
  <aside class="sidebar">
    <div class="search-container">
      <input
        type="text"
        v-model="searchTerm"
        class="search-box"
        placeholder="Search..."
        @input="updateSearch"
      />
      <button class="clear-btn" @click="clearSearch">&times;</button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #f4f4f4;
}

.search-container {
  position: relative;
  width: 100%;
}

.search-box {
  width: 100%;
  padding: 10px 40px 10px 20px;
  border-radius: 25px;
  border: 1px solid #ccc;
  outline: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: border 0.3s ease;
}

.search-box:focus {
  border: 1px solid #007bff;
}

.clear-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #999;
  outline: none;
}

.clear-btn:hover {
  color: #007bff;
}
</style>
