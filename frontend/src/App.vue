<script setup>
import { ref } from "vue";
import nlp from "compromise";
import axiosInstance from "./utils/axiosInstance";

let searchValue = ref("");
let isActiveKeywordSearch = ref(false);

let keywords = [];
let querySearchData = [];

const querySearchUrl = "/search-images";
const keywordSearchUrl = "/search-products";

let querySearchPayload = {
  text: searchValue.value,
};

let keywordSearchPayload = {
  query: "string",
  limit: 10,
  offset: 0,
  filter: [],
  sort: []
};

const fetchSearchValue = () => {
  if (isActiveKeywordSearch.value === true) {
    keywords = extractKeywords(searchValue.value);
  }

  fetchData(querySearchUrl, querySearchPayload).then((data) => {
    if (data) {
      querySearchData = data;
    } else {
      console.log("Failed to fetch data.");
    }
  });
};

function extractKeywords(sentence) {
  const doc = nlp(sentence);

  // Extract nouns and verbs as keywords
  const keywords = doc.nouns().out("array").concat(doc.verbs().out("array"));

  return keywords;
}

async function fetchData(url, payload) {
  try {
    const response = await axiosInstance.post(url, payload);
    const data = response.data;
    return data;
  } catch (error) {
    console.error("Error posting data:", error);
    return null;
  }
}
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
            <!--end of col-->
            <div class="col">
              <input
                class="form-control form-control-lg form-control-borderless"
                type="search"
                placeholder="What are you looking for ?"
                v-model="searchValue"
              />
            </div>
            <!--end of col-->
            <div class="col-auto">
              <button class="btn btn-lg btn-success" type="submit">
                Search
              </button>
            </div>
            <!--end of col-->
            <div class="col-auto form-check">
              <input
                type="checkbox"
                class="btn-check"
                id="btn-check-5"
                autocomplete="off"
                v-model="isActiveKeywordSearch"
              />
              <label class="btn" for="btn-check-5">KeywordSearch</label>
            </div>

            <!--end of col-->
          </div>
        </form>
      </div>
      <!--end of col-->
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
