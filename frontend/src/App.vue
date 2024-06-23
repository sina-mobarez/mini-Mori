<script setup>
import { ref } from "vue";
import nlp from 'compromise';


let searchValue = ref("");
let isActiveKeywordSearch = ref(false);

let keywords = []

const getSearchValue = () => {
  if (isActiveKeywordSearch.value === true) {
    keywords = extractKeywords(searchValue.value);
  }

};

function extractKeywords(sentence) {
  const doc = nlp(sentence);

  // Extract nouns and verbs as keywords
  const keywords = doc
    .nouns()
    .out('array')
    .concat(doc.verbs().out('array'));

  return keywords;
}

</script>

<template>
  <div class="container">
    <br />
    <div class="row justify-content-center">
      <div class="col-12 col-md-10 col-lg-8">
        <form @submit.prevent="getSearchValue" class="card card-sm">
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
