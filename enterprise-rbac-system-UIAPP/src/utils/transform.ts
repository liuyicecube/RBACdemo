export const transformKeysToSnake = (obj: any): any => {
  if (Array.isArray(obj)) {
    return obj.map(transformKeysToSnake)
  }
  if (obj && typeof obj === 'object') {
    const result: any = {}
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        const snakeKey = key.replace(/([A-Z])/g, '_$1').toLowerCase()
        result[snakeKey] = transformKeysToSnake(obj[key])
      }
    }
    return result
  }
  return obj
}

export const transformKeysToCamel = (obj: any): any => {
  if (Array.isArray(obj)) {
    return obj.map(transformKeysToCamel)
  }
  if (obj && typeof obj === 'object') {
    const result: any = {}
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        const camelKey = key.replace(/_(\w)/g, (_, c) => c.toUpperCase())
        result[camelKey] = transformKeysToCamel(obj[key])
      }
    }
    return result
  }
  return obj
}
