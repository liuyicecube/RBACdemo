import { describe, it, expect } from 'vitest'
import { transformKeysToSnake, transformKeysToCamel } from '../transform'

describe('transform utility', () => {
  describe('transformKeysToSnake', () => {
    it('should transform camelCase keys to snake_case', () => {
      const input = {
        userName: 'test',
        userEmail: 'test@example.com',
        isActive: true,
        createdAt: '2024-01-01'
      }
      const output = transformKeysToSnake(input)
      expect(output).toEqual({
        user_name: 'test',
        user_email: 'test@example.com',
        is_active: true,
        created_at: '2024-01-01'
      })
    })

    it('should handle nested objects', () => {
      const input = {
        userInfo: {
          firstName: 'John',
          lastName: 'Doe'
        }
      }
      const output = transformKeysToSnake(input)
      expect(output).toEqual({
        user_info: {
          first_name: 'John',
          last_name: 'Doe'
        }
      })
    })

    it('should handle arrays', () => {
      const input = {
        userList: [
          { userName: 'user1' },
          { userName: 'user2' }
        ]
      }
      const output = transformKeysToSnake(input)
      expect(output).toEqual({
        user_list: [
          { user_name: 'user1' },
          { user_name: 'user2' }
        ]
      })
    })

    it('should return null if input is null', () => {
      expect(transformKeysToSnake(null)).toBeNull()
    })

    it('should return undefined if input is undefined', () => {
      expect(transformKeysToSnake(undefined)).toBeUndefined()
    })
  })

  describe('transformKeysToCamel', () => {
    it('should transform snake_case keys to camelCase', () => {
      const input = {
        user_name: 'test',
        user_email: 'test@example.com',
        is_active: true,
        created_at: '2024-01-01'
      }
      const output = transformKeysToCamel(input)
      expect(output).toEqual({
        userName: 'test',
        userEmail: 'test@example.com',
        isActive: true,
        createdAt: '2024-01-01'
      })
    })

    it('should handle nested objects', () => {
      const input = {
        user_info: {
          first_name: 'John',
          last_name: 'Doe'
        }
      }
      const output = transformKeysToCamel(input)
      expect(output).toEqual({
        userInfo: {
          firstName: 'John',
          lastName: 'Doe'
        }
      })
    })

    it('should handle arrays', () => {
      const input = {
        user_list: [
          { user_name: 'user1' },
          { user_name: 'user2' }
        ]
      }
      const output = transformKeysToCamel(input)
      expect(output).toEqual({
        userList: [
          { userName: 'user1' },
          { userName: 'user2' }
        ]
      })
    })
  })
})
