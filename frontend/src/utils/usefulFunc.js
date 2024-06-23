import axiosInstance from "./axiosInstance";
import nlp from "compromise";

export function extractIds(objects) {
  return objects.map((obj) => obj.id);
}

export function extractKeywords(sentence) {
  const doc = nlp(sentence);

  // Extract nouns and verbs as keywords
  const keywords = doc.nouns().out("array").concat(doc.verbs().out("array"));

  return keywords;
}

export async function fetchData(url, payload) {
  try {
    const response = await axiosInstance.post(url, {"text":payload});
    const data = response.data;
    return data;
  } catch (error) {
    console.error("Error posting data:", error);
    return null;
  }
}

export async function fetchProductsByIds(ids, url) {
  try {
    const queryString = ids.map((id) => `ids=${id}`).join("&");
    const builturl = `${url}?${queryString}`;

    const response = await axiosInstance.get(builturl);
    return response.data;
  } catch (error) {
    console.error("Error fetching products:", error);
    throw new Error("Failed to fetch products.");
  }
}

