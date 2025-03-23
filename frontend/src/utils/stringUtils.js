// Create new file for utility functions
export const normalizeTestName = (name) => {
  return name
    .toLowerCase()
    // Remove special characters and extra spaces
    .replace(/[^a-z0-9\s]/g, '')
    .trim()
    // Split into words, sort them, and rejoin
    .split(/\s+/)
    .sort()
    .join('');
};

export const normalizeChars = (name) => {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '')
    .split('')
    .sort()
    .join('');
};

export const areTestNamesSimilar = (name1, name2) => {
  // First try exact word-order match
  const normWords1 = normalizeTestName(name1);
  const normWords2 = normalizeTestName(name2);
  
  if (normWords1 === normWords2) return true;
  
  // Then try character-level match
  const normChars1 = normalizeChars(name1);
  const normChars2 = normalizeChars(name2);
  
  // If one is significantly shorter, don't match
  const lengthRatio = Math.min(normChars1.length, normChars2.length) / 
                     Math.max(normChars1.length, normChars2.length);
  
  // Only consider character matching if lengths are similar (80% or more)
  if (lengthRatio >= 0.8) {
    // Check if character sets are identical
    if (normChars1 === normChars2) return true;
    
    // Check if one is contained within the other
    if (normChars1.includes(normChars2) || normChars2.includes(normChars1)) return true;
  }
  
  return false;
};
