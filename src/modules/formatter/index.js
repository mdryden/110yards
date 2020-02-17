export const formatScore = score => {
  return new Intl.NumberFormat("en-CA", {
    minimumFractionDigits: 2,
  }).format(score)
}
