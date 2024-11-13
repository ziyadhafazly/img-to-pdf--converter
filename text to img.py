import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

class TextToPDFConverter(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Text to PDF Converter")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")

        # Style configuration
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", 
                           padding=10, 
                           font=("Arial", 10, "bold"))
        self.style.configure("Custom.TLabel", 
                           font=("Arial", 12),
                           padding=5)

        self.create_widgets()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, 
                              text="Text to PDF Converter",
                              font=("Arial", 20, "bold"),
                              style="Custom.TLabel")
        title_label.pack(pady=10)

        # Text area frame
        text_frame = ttk.LabelFrame(main_frame, text="Enter your text", padding="10")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Text area with scrollbar
        self.text_area = tk.Text(text_frame, 
                                wrap=tk.WORD,
                                font=("Arial", 11),
                                bg="white",
                                height=15)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        # Clear button
        clear_btn = ttk.Button(button_frame, 
                             text="Clear Text",
                             style="Custom.TButton",
                             command=self.clear_text)
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Save button
        save_btn = ttk.Button(button_frame, 
                            text="Save as PDF",
                            style="Custom.TButton",
                            command=self.save_as_pdf)
        save_btn.pack(side=tk.RIGHT, padx=5)

        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(main_frame, 
                             textvariable=self.status_var,
                             font=("Arial", 10),
                             foreground="gray")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def clear_text(self):
        self.text_area.delete(1.0, tk.END)
        self.status_var.set("Text cleared")

    def save_as_pdf(self):
        text_content = self.text_area.get(1.0, tk.END).strip()
        
        if not text_content:
            messagebox.showwarning("Warning", "Please enter some text before saving!")
            return

        try:
            # Get file path from user
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Save PDF As"
            )

            if file_path:
                # Create PDF
                c = canvas.Canvas(file_path, pagesize=A4)
                width, height = A4
                
                # Split text into lines
                y = height - 50  # Start from top with margin
                lines = text_content.split('\n')
                
                for line in lines:
                    # Word wrap for long lines
                    words = line.split()
                    current_line = ''
                    
                    for word in words:
                        if c.stringWidth(current_line + ' ' + word) < width - 100:
                            current_line += ' ' + word
                        else:
                            c.drawString(50, y, current_line.strip())
                            y -= 20
                            current_line = word
                            
                            # Check if we need a new page
                            if y < 50:
                                c.showPage()
                                y = height - 50
                    
                    if current_line:
                        c.drawString(50, y, current_line.strip())
                        y -= 20
                    
                    # Add line break
                    y -= 5
                    
                    # Check if we need a new page
                    if y < 50:
                        c.showPage()
                        y = height - 50

                c.save()
                
                self.status_var.set(f"PDF saved successfully: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "PDF file has been created successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error occurred while saving PDF")

if __name__ == "__main__":
    app = TextToPDFConverter()
    app.mainloop()
