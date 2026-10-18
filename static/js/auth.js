/**
 * Auth page helpers: password visibility toggle only.
 * Form submits normally to Django (CSRF + server validation).
 */
function togglePasswordVisibility(inputId, eyeId, eyeSlashId) {
  var input = document.getElementById(inputId || "id_password");
  var eye = document.getElementById(eyeId || "eye-icon");
  var eyeSlash = document.getElementById(eyeSlashId || "eye-slash-icon");
  if (!input) return;
  var isPassword = input.type === "password";
  input.type = isPassword ? "text" : "password";
  if (eye) eye.classList.toggle("hidden", isPassword);
  if (eyeSlash) eyeSlash.classList.toggle("hidden", !isPassword);
}

function togglePasswordVisibilitySimple() {
  togglePasswordVisibility("id_password", "eye-icon", "eye-slash-icon");
}

function togglePasswordVisibility2() {
  togglePasswordVisibility("id_password2", "eye-icon-2", "eye-slash-icon-2");
}
