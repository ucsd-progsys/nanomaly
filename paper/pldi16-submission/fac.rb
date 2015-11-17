def factorial(n)
  if n <= 0
    true
  else
    n * factorial(n-1)
  end
end

factorial(1)
