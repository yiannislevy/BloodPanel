// Create new file for utility functions
export const normalizeTestName = (name) => {
  return name
    .toLowerCase()
    // Remove special characters and extra spaces
    .replace(/[^a-z0-9]/g, '')
    .trim();
};

export const areTestNamesSimilar = (name1, name2) => {
  return normalizeTestName(name1) === normalizeTestName(name2);
}; 