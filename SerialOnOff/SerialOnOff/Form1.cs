using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace SerialOnOff
{
    public partial class mainForm : Form
    {
        private static int IPC_PORT = 1;
        private static IPC _ipc;

        public mainForm()
        {
            InitializeComponent();

            _ipc = new IPC(IPC_PORT);
        }

       

        private void mainForm_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            BackColor = Color.Green;
            _ipc.SendOn();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            BackColor = Color.Red;
            _ipc.SendOFF();
        }
    }
}
