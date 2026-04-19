import { describe, it, expect } from 'vitest'
import { formatDate, formatDateTime, formatRelativeTime } from '../date'

describe('date utility', () => {
  describe('formatDate', () => {
    it('should format date to YYYY-MM-DD', () => {
      const date = new Date('2024-01-15')
      expect(formatDate(date)).toBe('2024-01-15')
    })

    it('should format date string', () => {
      expect(formatDate('2024-01-15T12:00:00')).toBe('2024-01-15')
    })

    it('should handle null and return empty string', () => {
      expect(formatDate(null)).toBe('')
    })

    it('should handle undefined and return empty string', () => {
      expect(formatDate(undefined)).toBe('')
    })
  })

  describe('formatDateTime', () => {
    it('should format datetime to YYYY-MM-DD HH:mm:ss', () => {
      const date = new Date('2024-01-15T14:30:45')
      expect(formatDateTime(date)).toBe('2024-01-15 14:30:45')
    })

    it('should format datetime string', () => {
      expect(formatDateTime('2024-01-15T14:30:45')).toBe('2024-01-15 14:30:45')
    })
  })

  describe('formatRelativeTime', () => {
    it('should format relative time for just now', () => {
      const date = new Date()
      expect(formatRelativeTime(date)).toContain('刚刚')
    })

    it('should format relative time for minutes ago', () => {
      const date = new Date(Date.now() - 5 * 60 * 1000)
      expect(formatRelativeTime(date)).toContain('分钟前')
    })

    it('should format relative time for hours ago', () => {
      const date = new Date(Date.now() - 2 * 60 * 60 * 1000)
      expect(formatRelativeTime(date)).toContain('小时前')
    })

    it('should format relative time for days ago', () => {
      const date = new Date(Date.now() - 3 * 24 * 60 * 60 * 1000)
      expect(formatRelativeTime(date)).toContain('天前')
    })
  })
})
