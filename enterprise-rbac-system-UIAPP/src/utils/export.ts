export const exportToCSV = (data: any[], filename: string, headers?: { key: string; title: string }[]) => {
  if (!data || data.length === 0) {
    return
  }

  let csvContent = ''
  let keys: string[] = []

  if (headers && headers.length > 0) {
    csvContent = headers.map(h => h.title).join(',') + '\n'
    keys = headers.map(h => h.key)
  } else {
    const firstRow = data[0]
    keys = Object.keys(firstRow)
    csvContent = keys.join(',') + '\n'
  }

  data.forEach(row => {
    const values = keys.map(key => {
      let value = row[key]
      if (value === null || value === undefined) {
        return ''
      }
      if (typeof value === 'string') {
        if (value.includes(',') || value.includes('"') || value.includes('\n')) {
          value = '"' + value.replace(/"/g, '""') + '"'
        }
      }
      return value
    })
    csvContent += values.join(',') + '\n'
  })

  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `${filename}.csv`)
  link.style.display = 'none'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

export const exportToJSON = (data: any[], filename: string) => {
  const jsonContent = JSON.stringify(data, null, 2)
  const blob = new Blob([jsonContent], { type: 'application/json' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  link.setAttribute('href', url)
  link.setAttribute('download', `${filename}.json`)
  link.style.display = 'none'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}



export const debounce = <T extends (...args: any[]) => any>(func: T, wait: number): ((...args: Parameters<T>) => void) => {
  let timeout: any = null
  return (...args: Parameters<T>) => {
    if (timeout) {
      clearTimeout(timeout)
    }
    timeout = setTimeout(() => func(...args), wait)
  }
}

export const throttle = <T extends (...args: any[]) => any>(func: T, wait: number): ((...args: Parameters<T>) => void) => {
  let lastTime = 0
  return (...args: Parameters<T>) => {
    const now = Date.now()
    if (now - lastTime >= wait) {
      lastTime = now
      func(...args)
    }
  }
}

export const deepClone = <T>(obj: T): T => {
  if (obj === null || typeof obj !== 'object') {
    return obj
  }
  if (obj instanceof Date) {
    return new Date(obj.getTime()) as unknown as T
  }
  if (obj instanceof Array) {
    return obj.map(item => deepClone(item)) as unknown as T
  }
  if (typeof obj === 'object') {
    const clonedObj = {} as Record<string, any>
    for (const key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
        clonedObj[key] = deepClone((obj as any)[key])
      }
    }
    return clonedObj as T
  }
  return obj
}

export const buildTree = <T extends { id: number; parentId?: number | null }>(
  list: T[],
  parentId: number | null = null
): T[] => {
  const tree: T[] = []
  const map = new Map<number, T & { children?: T[] }>()

  list.forEach(item => {
    map.set(item.id, { ...item, children: [] })
  })

  list.forEach(item => {
    const node = map.get(item.id)!
    if (item.parentId === parentId) {
      tree.push(node)
    } else {
      const parent = map.get(item.parentId as number)
      if (parent) {
        parent.children!.push(node)
      } else {
        tree.push(node)
      }
    }
  })

  return tree
}

export const flattenTree = <T extends { children?: T[] }>(tree: T[]): T[] => {
  const result: T[] = []
  const traverse = (nodes: T[]) => {
    nodes.forEach(node => {
      const { children, ...rest } = node
      result.push(rest as T)
      if (children && children.length > 0) {
        traverse(children)
      }
    })
  }
  traverse(tree)
  return result
}

export const getTreeIds = <T extends { id: number; children?: T[] }>(tree: T[]): number[] => {
  const ids: number[] = []
  const traverse = (nodes: T[]) => {
    nodes.forEach(node => {
      ids.push(node.id)
      if (node.children && node.children.length > 0) {
        traverse(node.children)
      }
    })
  }
  traverse(tree)
  return ids
}
