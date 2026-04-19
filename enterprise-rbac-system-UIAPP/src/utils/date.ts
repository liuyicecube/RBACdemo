/**
 * 日期格式化工具
 */

/**
 * 格式化日期时间
 * @param date 日期对象或日期字符串
 * @param format 格式化模式，默认 'YYYY-MM-DD HH:mm:ss'
 * @returns 格式化后的日期字符串
 */
export function formatDateTime(date: Date | string | number | null | undefined, format: string = 'YYYY-MM-DD HH:mm:ss'): string {
  if (!date) {
    return '-'
  }

  let dateObj: Date
  if (typeof date === 'string') {
    // 处理各种日期字符串格式
    try {
      // 尝试直接解析
      dateObj = new Date(date)
      if (!isNaN(dateObj.getTime())) {
        // 成功解析
      } else {
        // 尝试解析为本地时间字符串
        dateObj = new Date(date.replace('T', ' ').replace('Z', ''))
      }
    } catch {
      return '-'
    }
  } else if (typeof date === 'number') {
    dateObj = new Date(date)
  } else {
    dateObj = date
  }

  // 检查日期是否有效
  if (isNaN(dateObj.getTime())) {
    return '-'
  }

  const year = dateObj.getFullYear()
  const month = String(dateObj.getMonth() + 1).padStart(2, '0')
  const day = String(dateObj.getDate()).padStart(2, '0')
  const hours = String(dateObj.getHours()).padStart(2, '0')
  const minutes = String(dateObj.getMinutes()).padStart(2, '0')
  const seconds = String(dateObj.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', String(year))
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 格式化日期（仅日期部分）
 * @param date 日期对象或日期字符串
 * @param format 格式化模式，默认 'YYYY-MM-DD'
 * @returns 格式化后的日期字符串
 */
export function formatDate(date: Date | string | number | null | undefined, format?: string): string {
  return formatDateTime(date, format || 'YYYY-MM-DD')
}

/**
 * 格式化时间（仅时间部分）
 * @param date 日期对象或日期字符串
 * @returns 格式化后的时间字符串
 */
export function formatTime(date: Date | string | number | null | undefined): string {
  return formatDateTime(date, 'HH:mm:ss')
}
