export function isValidJwt (jwt: string) {
  return !!jwt;
}

export const DialogError = {
  title: 'Ошибка',
  message: '',
  type: 'is-danger',
};