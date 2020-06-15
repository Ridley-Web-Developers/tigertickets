<template>
    <div id="app">
        <div class="main-container">
            <div id="nav">
                <b-navbar id="nav_bar" toggleable="md">
                    <b-navbar-brand style="padding-top: 0; padding-bottom: 0; margin-left: 0.375rem" to="/"><img
                            alt="Logo"
                            src="@/assets/logo.jpg" style="height: 60px; margin: 5px"/></b-navbar-brand>
                    <b-navbar-toggle id="collapse-button" target="nav-collapse"></b-navbar-toggle>
                    <b-collapse id="nav-collapse" is-nav>
                        <!--add class="ml-auto" to align right-->
                        <b-navbar-nav>
                            <b-nav-item to="/">Home</b-nav-item>
                            <b-nav-item to="/about">About</b-nav-item>
                            <b-nav-item to="/events">Events</b-nav-item>
                        </b-navbar-nav>
                        <b-navbar-nav class="ml-auto">
                            <b-nav-item-dropdown class="nav-item" text="You are not logged in" right>
                                <b-dropdown-item varient="dark" class="nav-item" to="/about"><span
                                        class="dropdown-text">Sign in</span></b-dropdown-item>
                                <b-dropdown-divider/>
                                <b-dropdown-item class="nav-item" href="#"><span
                                        class="dropdown-text">Sign up</span></b-dropdown-item>
                            </b-nav-item-dropdown>
                        </b-navbar-nav>
                    </b-collapse>
                </b-navbar>
            </div>
            <br>
            <div class="parent">
                <div class="background-layer">
                    <br>
                    <router-view/>
                    <br>
                </div>
            </div>
            <br>
        </div>
        <footer class="page-footer font-small footer">
            <div class="footer-copyright text-center footer-text">
                <small style="color: #f1f1f1">© Mandeville Theatre Online Ticket Selling System Developer Team</small>
            </div>
        </footer>
    </div>
</template>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        background-image: url("./assets/mainbackground.png");
        background-repeat: no-repeat;
        background-position: center; /* Center the image */
        background-size: cover; /* Resize the background image to cover the entire container */
    }

    #nav_bar {
        z-index: 10;
        font-size: 22px;
        background-color: #333333;
        position: sticky;
        top: 0;
        height: 100%;
        width: 100%;
    }

    #nav a {
        font-weight: bold;
        color: #f1f1f1;
    }

    .main-container {
        min-height: 100vh;
    }

    .background-layer {
        background: rgba(255, 255, 255, 0.6);
        width: 80%;
        max-width: 80%;
        border-radius: 10px
    }

    .parent {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .footer {
        background-color: #333333;
        height: 60px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .dropdown-text {
        color: #333333 !important;
        font-size: 22px;
    }
</style>
