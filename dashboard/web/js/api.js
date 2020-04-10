class Api {
  getSecurityConfig(callback) {
    axios.get("http://192.168.86.250:5250/config").then((response) => {
      callback(response.data);
    });
  }
}
