Maudiel Romero: mar641
Alex Miller: arm297

Client function:
What we did for the client was connect to both servers, then while it still was connected and had lines to read in the Hostname text document we would first check with the rs server to see if they contained that hostname. If it didn't, then we had the client send a request to the ts server and again check if it contained the hostname. Ultimately if neither had it we had ts send back the error message and client would then move on till it hit it's last line then it would close.

Known issues:


Problems we faced:
One problem we faced was testing on Ilab machines and on our separate devices. We coded on our locals and ran into some issues when trying to test on ilabs or Maudiel's code not working properly on my machine.

What we learned:
We learned about multiple socket programming, This wasn't all that different from the first so it was good training again for socket programming. And finally we learned about how different machines can have different settings and the same code might not work on another. We will probably try and test more often on ilabs than we did this time.
