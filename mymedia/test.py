import smtplib

server = smtplib.SMTP("smtp.naver.com", 587)
server.starttls()
server.login("wavecanon@naver.com", "SNMQEN583GSC")
print("로그인 성공")
server.quit()
