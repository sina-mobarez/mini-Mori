<script setup>
import { ref } from "vue";
import {
  extractIds,
  fetchData,
  extractKeywords,
  fetchProductsByIds,
} from "./utils/usefulFunc";

// Define reactive properties
let searchValue = ref("");
let isActiveKeywordSearch = ref(false);
let products = ref([]); // Make products reactive

let keywords = [];
let querySearchData = [];

const querySearchUrl = "/search-images";
const keywordSearchByIdsUrl = "/search-products-by-ids";


// Function to fetch and process search value
const fetchSearchValue = async () => {
  try {
    // Fetch data based on query search
    const data = await fetchData(querySearchUrl, searchValue.value);
    if (data) {
      console.log(data);
      let productIds = extractIds(data);

      // Fetch products by their IDs
      const fetchedProducts = await fetchProductsByIds(
        productIds,
        keywordSearchByIdsUrl
      );
      if (fetchedProducts) {
        console.log(searchValue.value);
        products.value = fetchedProducts; // Update products array
        searchValue.value = '';
        console.log(productIds);
      } else {
        console.log("Failed to fetch products by IDs.");
      }
    } else {
      console.log("Failed to fetch data.");
    }

    // If keyword search is active, process keywords
    if (isActiveKeywordSearch.value === true) {
      keywords = extractKeywords(searchValue.value);
      // You can add additional logic for keyword search here if needed
    }
  } catch (error) {
    console.error("Error fetching search value:", error);
  }
};
</script>

<template>
  <div class="container">
    <br />
    <div class="row justify-content-center">
      <div class="col-12 col-md-10 col-lg-8">
        <form @submit.prevent="fetchSearchValue" class="card card-sm">
          <div class="card-body row no-gutters align-items-center">
            <div class="col-auto">
              <i class="fas fa-search h4 text-body"></i>
            </div>
            <div class="col">
              <input
                class="form-control form-control-lg form-control-borderless"
                type="search"
                placeholder="What are you looking for?"
                v-model="searchValue"
              />
            </div>
            <div class="col-auto">
              <button class="btn btn-lg btn-success" type="submit">
                Search
              </button>
            </div>
            <div class="col-auto form-check">
              <input
                type="checkbox"
                class="btn-check"
                id="btn-check-5"
                autocomplete="off"
                v-model="isActiveKeywordSearch"
              />
              <label class="btn" for="btn-check-5">Keyword Search</label>
            </div>
          </div>
        </form>
      </div>
    </div>
    <div class="row justify-content-center mt-3">
      <div
        v-for="(product, index) in products"
        :key="index"
        class="card m-3"
        style="width: 18rem"
      >
        <img
          v-if="product.images && product.images.length > 0"
          :src="product.images[0]"
          class="card-img-top"
          alt="Product Image"
        />
        <div class="card-body">
          <h5 class="card-title">{{ product.name }}</h5>
          <p class="card-text">{{ product.description }}</p>
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">{{ product.current_price }}</li>
          <li class="list-group-item">{{ product.shop_name }}</li>
        </ul>
        <div class="card-body">
          <a :href="product.link" class="card-link">Product link</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.form-control-borderless {
  border: none;
}

.form-control-borderless:hover,
.form-control-borderless:active,
.form-control-borderless:focus {
  border: none;
  outline: none;
  box-shadow: none;
}
</style>
