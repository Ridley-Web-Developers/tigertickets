<template>
  <div class="home">
    <Signup></Signup>
  </div>
</template>

<script>
// @ is an alias to /src

import Signup from "../components/Signup";

export default {
  name: 'Home',
  components: {
    Signup,
  }
}
</script>
