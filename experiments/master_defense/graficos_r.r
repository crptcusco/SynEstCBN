library(ggplot2)
library(readr)
#data<-read_delim(file.choose(),delim = "\t"):
scaleFUN <- function(x) sprintf("%.2f", x)

#tabla1 <- read.table('tabla1.txt', header = TRUE, sep ='\t',dec = ',')
tabla1 <- read.table('//home//dimitruss//Dropbox//RESEARCH//FILES//experimentos//tabla1.txt', header = TRUE, sep ='\t',dec = ',')
head(tabla1)
ggplot(tabla1, aes(x = redes, y = tempo) ) +
  xlab("numero de redes") +
  ylab("tempo (seg.)") +
  scale_y_continuous(labels=scaleFUN) +
  geom_point() +    # Use hollow circles
  geom_smooth(method=lm,se=FALSE)   # Add linear regression line 

#tabla2 <- read.table('tabla2.txt', header = TRUE, sep ='\t',dec = ',')
tabla2 <- read.table('//home//dimitruss//Dropbox//RESEARCH//FILES//experimentos//tabla2.txt', header = TRUE, sep ='\t',dec = ',')
ggplot(tabla2, aes(x = variaveis, y = tempo))+
  xlab("numero de variaveis") +
  ylab("tempo (seg.)") +
  scale_y_continuous(labels=scaleFUN) +
  geom_point()+
  geom_smooth(se=FALSE)

#tabla3 <- read.table('tabla3.txt', header = TRUE, sep ='\t',dec = ',')
tabla3 <- read.table('//home//dimitruss//Dropbox//RESEARCH//FILES//experimentos//tabla3.txt', header = TRUE, sep ='\t',dec = ',')
ggplot(tabla3, aes(x = constantes, y = tempo)) +
  xlab("numero de sinais de acoplamento") +
  ylab("tempo (seg.)") +
  scale_y_continuous(labels=scaleFUN) +
  geom_point()+
  geom_smooth(se=FALSE)
