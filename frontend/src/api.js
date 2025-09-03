import axios from 'axios';

export async function askFromBackend(userInput) {
  try {
    const response = await axios.post("http://127.0.0.1:8000/query", {
      query: userInput
    });

    return {
      answer: response.data.answer,
      link: response.data.link || ''
    };
  } catch (error) {
    console.error("Backend responded with:", error.response.status, error.response.data);
    console.error("Error contacting backend:", error);
    return {
      answer: "There was an issue reaching the server. Please try again later.",
      link: ''
    };
  }
}
