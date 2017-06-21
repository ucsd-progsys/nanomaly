library(irr)

a0 = read.csv(file="study-data/A-0-scores.csv")
a1 = read.csv(file="study-data/A-1-scores.csv")
a2 = read.csv(file="study-data/A-2-scores.csv")
a3 = read.csv(file="study-data/A-Eric-scores.csv")
b0 = read.csv(file="study-data/B-0-scores.csv")
b1 = read.csv(file="study-data/B-1-scores.csv")
b2 = read.csv(file="study-data/B-2-scores.csv")
b3 = read.csv(file="study-data/B-Eric-scores.csv")

reasons0 = c(a0$X1..append.reason,
             a0$X3..digitsofint.reason,
             a0$X5..sumlist.reason,
             a0$X7..wwhile.reason,
             b0$X1..sumlist.reason,
             b0$X3..wwhile.reason,
             b0$X5..append.reason,
             b0$X7..digitsofint.reason)
reasons1 = c(a1$X1..append.reason,
             a1$X3..digitsofint.reason,
             a1$X5..sumlist.reason,
             a1$X7..wwhile.reason,
             b1$X1..sumlist.reason,
             b1$X3..wwhile.reason,
             b1$X5..append.reason,
             b1$X7..digitsofint.reason)
reasons2 = c(a2$X1..append.reason,
             a2$X3..digitsofint.reason,
             a2$X5..sumlist.reason,
             a2$X7..wwhile.reason,
             b2$X1..sumlist.reason,
             b2$X3..wwhile.reason,
             b2$X5..append.reason,
             b2$X7..digitsofint.reason)
reasons3 = c(a3$X1..append.reason,
             a3$X3..digitsofint.reason,
             a3$X5..sumlist.reason,
             a3$X7..wwhile.reason,
             b3$X1..sumlist.reason,
             b3$X3..wwhile.reason,
             b3$X5..append.reason,
             b3$X7..digitsofint.reason)
reasons = data.frame(reasons0, reasons1, reasons2, reasons3)
## filter out answers that any annotator marked as INCOMPLETE
reasons = reasons[reasons$reasons0 != -1 & reasons$reasons1 != -1 & reasons$reasons2 != -1 & reasons$reasons3 != -1,]

fixes0 = c(a0$X2..append.fix,
           a0$X4..digitsofint.fix,
           a0$X6..sumlist.fix,
           a0$X8..wwhile.fix,
           b0$X2..sumlist.fix,
           b0$X4..wwhile.fix,
           b0$X6..append.fix,
           b0$X8..digitsofint.fix)
fixes1 = c(a1$X2..append.fix,
           a1$X4..digitsofint.fix,
           a1$X6..sumlist.fix,
           a1$X8..wwhile.fix,
           b1$X2..sumlist.fix,
           b1$X4..wwhile.fix,
           b1$X6..append.fix,
           b1$X8..digitsofint.fix)
fixes2 = c(a2$X2..append.fix,
           a2$X4..digitsofint.fix,
           a2$X6..sumlist.fix,
           a2$X8..wwhile.fix,
           b2$X2..sumlist.fix,
           b2$X4..wwhile.fix,
           b2$X6..append.fix,
           b2$X8..digitsofint.fix)
fixes3 = c(a3$X2..append.fix,
           a3$X4..digitsofint.fix,
           a3$X6..sumlist.fix,
           a3$X8..wwhile.fix,
           b3$X2..sumlist.fix,
           b3$X4..wwhile.fix,
           b3$X6..append.fix,
           b3$X8..digitsofint.fix)
fixes = data.frame(fixes0, fixes1, fixes2, fixes3)
## filter out answers that any annotator marked as INCOMPLETE
fixes = fixes[fixes$fixes0 != -1 & fixes$fixes1 != -1 & fixes$fixes2 != -1 & fixes$fixes3 != -1,]

print("REASONS")
print(reasons[,1])
print(reasons[,2])
print(reasons[,3])
print(reasons[,4])
print(kappam.fleiss(reasons,exact=TRUE,detail=TRUE))
#print(kappam.fleiss(reasons[1:3],detail=TRUE))

print("FIXES")
print(table(fixes[,1]))
print(table(fixes[,2]))
print(table(fixes[,3]))
print(table(fixes[,4]))
print(kappam.fleiss(fixes,exact=TRUE,detail=TRUE))
#print(kappam.fleiss(fixes[1:3],detail=TRUE))

significance <- function(x,y) {
  print(x)
  print(mean(x))
  print(y)
  print(mean(y))
  wilcox.test(x, y, alternative="g")
}

print("append reason")
print(significance(
        b3$X5..append.reason[b3$X5..append.reason != -1],
        a3$X1..append.reason[a3$X1..append.reason != -1]
))

print("digistofint reason")
print(significance(
        b3$X7..digitsofint.reason[b3$X7..digitsofint.reason != -1],
        a3$X3..digitsofint.reason[a3$X3..digitsofint.reason != -1]
))

print("sumlist reason")
print(significance(
        a3$X5..sumlist.reason[a3$X5..sumlist.reason != -1],
        b3$X1..sumlist.reason[b3$X1..sumlist.reason != -1]
))

print("wwhile reason")
print(significance(
        a3$X7..wwhile.reason[a3$X7..wwhile.reason != -1],
        b3$X3..wwhile.reason[b3$X3..wwhile.reason != -1]
))

print("append fix")
print(significance(
        b3$X6..append.fix[b3$X6..append.fix != -1],
        a3$X2..append.fix[a3$X2..append.fix != -1]
))

print("digistofint fix")
print(significance(
        b3$X8..digitsofint.fix[b3$X8..digitsofint.fix != -1],
        a3$X4..digitsofint.fix[a3$X4..digitsofint.fix != -1]
))

print("sumlist fix")
print(significance(
        a3$X6..sumlist.fix[a3$X6..sumlist.fix != -1],
        b3$X2..sumlist.fix[b3$X2..sumlist.fix != -1]
))

print("wwhile fix")
print(significance(
        a3$X8..wwhile.fix[a3$X8..wwhile.fix != -1],
        b3$X4..wwhile.fix[b3$X4..wwhile.fix != -1]
))

# print("append")
# print(significance(
#         c(b3$X5..append.reason[b3$X5..append.reason != -1],
#           b3$X6..append.fix[b3$X6..append.fix != -1]),
#         c(a3$X1..append.reason[a3$X1..append.reason != -1],
#           a3$X2..append.fix[a3$X2..append.fix != -1])
# ))

# print("digistofint")
# print(significance(
#         c(b3$X7..digitsofint.reason[b3$X7..digitsofint.reason != -1],
#           b3$X8..digitsofint.fix[b3$X8..digitsofint.fix != -1]),
#         c(a3$X3..digitsofint.reason[a3$X3..digitsofint.reason != -1],
#           a3$X4..digitsofint.fix[a3$X4..digitsofint.fix != -1])
# ))

# print("sumlist")
# print(significance(
#         c(a3$X5..sumlist.reason[a3$X5..sumlist.reason != -1],
#           a3$X6..sumlist.fix[a3$X6..sumlist.fix != -1]),
#         c(b3$X1..sumlist.reason[b3$X1..sumlist.reason != -1],
#           b3$X2..sumlist.fix[b3$X2..sumlist.fix != -1])
# ))

# print("wwhile")
# print(significance(
#         c(a3$X7..wwhile.reason[a3$X7..wwhile.reason != -1],
#           a3$X8..wwhile.fix[a3$X8..wwhile.fix != -1]),
#         c(b3$X3..wwhile.reason[b3$X3..wwhile.reason != -1],
#           b3$X4..wwhile.fix[b3$X4..wwhile.fix != -1])
# ))

# print("total reason")
# print(significance(
#         c(b3$X5..append.reason[b3$X5..append.reason != -1],
#           b3$X7..digitsofint.reason[b3$X7..digitsofint.reason != -1],
#           a3$X5..sumlist.reason[a3$X5..sumlist.reason != -1],
#           a3$X7..wwhile.reason[a3$X7..wwhile.reason != -1]),
#         c(a3$X1..append.reason[a3$X1..append.reason != -1],
#           a3$X3..digitsofint.reason[a3$X3..digitsofint.reason != -1],
#           b3$X1..sumlist.reason[b3$X1..sumlist.reason != -1],
#           b3$X3..wwhile.reason[b3$X3..wwhile.reason != -1])
# ))

# print("total fix")
# print(significance(
#         c(b3$X6..append.fix[b3$X6..append.fix != -1],
#           b3$X8..digitsofint.fix[b3$X8..digitsofint.fix != -1],
#           a3$X6..sumlist.fix[a3$X6..sumlist.fix != -1],
#           a3$X8..wwhile.fix[a3$X8..wwhile.fix != -1]),
#         c(a3$X2..append.fix[a3$X2..append.fix != -1],
#           a3$X4..digitsofint.fix[a3$X4..digitsofint.fix != -1],
#           b3$X2..sumlist.fix[b3$X2..sumlist.fix != -1],
#           b3$X4..wwhile.fix[b3$X4..wwhile.fix != -1])
# ))

# print("total")
# print(significance(
#         c(b3$X5..append.reason[b3$X5..append.reason != -1],
#           b3$X7..digitsofint.reason[b3$X7..digitsofint.reason != -1],
#           a3$X5..sumlist.reason[a3$X5..sumlist.reason != -1],
#           a3$X7..wwhile.reason[a3$X7..wwhile.reason != -1],
#           b3$X6..append.fix[b3$X6..append.fix != -1],
#           b3$X8..digitsofint.fix[b3$X8..digitsofint.fix != -1],
#           a3$X6..sumlist.fix[a3$X6..sumlist.fix != -1],
#           a3$X8..wwhile.fix[a3$X8..wwhile.fix != -1]),
#         c(a3$X1..append.reason[a3$X1..append.reason != -1],
#           a3$X3..digitsofint.reason[a3$X3..digitsofint.reason != -1],
#           b3$X1..sumlist.reason[b3$X1..sumlist.reason != -1],
#           b3$X3..wwhile.reason[b3$X3..wwhile.reason != -1],
#           a3$X2..append.fix[a3$X2..append.fix != -1],
#           a3$X4..digitsofint.fix[a3$X4..digitsofint.fix != -1],
#           b3$X2..sumlist.fix[b3$X2..sumlist.fix != -1],
#           b3$X4..wwhile.fix[b3$X4..wwhile.fix != -1])
# ))
