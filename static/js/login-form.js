function register() {
    window.location.href = "{{ url_for('register') }}";
}
function login(){
    window.location.href = "{{ url_for('login') }}";
}