export function isValidJwt (jwt: string) {
  return !!jwt
}

export function getAccessToken() {
  return localStorage.getItem('access_token') as string;
}

export const DialogError = {
  title: 'Ошибка',
  message: '',
  type: 'is-danger',
};