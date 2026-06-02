import yfinance as yf
print("Program başladı")
hisse = yf.Ticker("THYAO.IS")
veri = hisse.history(period="5d")

print(veri.tail())

input("Çıkmak için Enter'a bas...")