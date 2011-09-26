using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.IO.Ports;

namespace SerialOnOff
{
    /// <summary>
    /// Class for communicating with IPC
    /// </summary>
    class IPC
    {
        private static byte[] ON = Encoding.ASCII.GetBytes("*PON");
        private static byte[] OFF = Encoding.ASCII.GetBytes("*POF");
        private static byte[] PING = Encoding.ASCII.GetBytes("*?PS");

        /// <summary>
        /// Check if an IPC is connected to the given port
        /// </summary>
        public static bool IsConnected(int port)
        {
            Mutex m = new Mutex(false, "SERIAL_PORT_" + port + "_MUTEX");
            SerialPort serialPort = new SerialPort("COM" + port, 300, Parity.None, 8, StopBits.One);
            try
            {
                serialPort.DtrEnable = !serialPort.DtrEnable;
                serialPort.Handshake = Handshake.None;
                serialPort.WriteTimeout = 100;
                serialPort.ReadTimeout = 100;
                m.WaitOne();
                serialPort.Open();
                serialPort.Write(PING, 0, PING.Length);
                string s = string.Empty;
                Thread.Sleep(1000);
                return serialPort.ReadExisting().Contains("$");
            }
            catch
            {
                return false;
            }
            finally
            {
                if (serialPort != null && serialPort.IsOpen)
                    serialPort.Close();
                m.ReleaseMutex();
            }
        }

        private readonly SerialPort serialPort;

        /// <summary>
        /// Initializes a new IPC on the specified port
        /// </summary>
        public IPC(int port)
        {
            if (IsConnected(port))
            {
                serialPort = new SerialPort("COM" + port, 300, Parity.None, 8, StopBits.One);
                serialPort.ReadTimeout = 1000;
                serialPort.DtrEnable = !serialPort.DtrEnable;
                serialPort.Handshake = Handshake.None;
                serialPort.Open();
            }
            else
            {
                serialPort = null;
                // throw new Exception("No IPC found on COM" + port.ToString());
            }
        }

        /// <summary>
        /// Power off the STB
        /// </summary>
        public void SendOFF()
        {
            if(serialPort != null)
                Send(OFF);
        }

        private void Send(byte[] message)
        {
            int failures = 0;
            while (true)
            {
                try
                {
                    serialPort.Write(message, 0, message.Length);
                    serialPort.ReadTo("$");
                    break;
                }
                catch
                {
                    if (++failures == 3)
                        throw new Exception("Lost communication with IPC, the device might be frozen or disconnected from the computer. To check if it is frozen try to initiate a power cycle manually by pressing the button on the device. If the device is frozen you will need to unplug it and plug it back in.");
                }
            }
        }

        /// <summary>
        /// Power on the STB
        /// </summary>
        public void SendOn()
        {
            if(serialPort != null)
                Send(ON);
        }
    }
}
