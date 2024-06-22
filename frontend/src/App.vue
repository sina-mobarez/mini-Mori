<script>
import Sidebar from "./components/Sidebar.vue";

export default {
  components: {
    Sidebar
  },
  data() {
    return {
      searchQuery: ''
    };
  },
  methods: {
    handleSearchUpdate(searchTerm) {
      this.searchQuery = searchTerm;
      console.log('Search term:', this.searchQuery); // For debugging purposes
      // You can also add any additional logic to handle the search term update here
    }
  }
};
</script>

<template>
  <sidebar>
    <div class="section section-30">
      <Sidebar @search-updated="handleSearchUpdate" />
    </div>
  </sidebar>

  <main>
    <div class="section section-70">
      <div class="content">
      <!-- Your main content goes here -->
      <p>Search Query: {{ searchQuery }}</p>
    </div>
    </div>
  </main>
</template>

<style scoped>
body {
  font-family: Arial, sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;
}

.container {
  display: flex;
  width: 80%;
  height: 60vh;
  border: 1px solid #ccc;
}

.section {
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.section-30 {
  flex: 0 0 30%;
  background-color: #cff6d8;
}

.section-70 {
  flex: 0 0 70%;
  background-color: #cce5ff;
}
</style>
